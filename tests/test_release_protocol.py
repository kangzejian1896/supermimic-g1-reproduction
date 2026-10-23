"""Regression checks for the release protocol, independent of private motion data."""
from pathlib import Path
from types import SimpleNamespace
import pytest
import torch
from supermimic.checkpoints import load_checkpoint, initialize_models
from supermimic.envs.tracking_env_cfg import make_env_cfg, SuperMimicEnvCfgArgs
from supermimic.eval.benchmark import ClipResult, summarize


def test_paper_protocol_is_opt_in():
    legacy = make_env_cfg(SuperMimicEnvCfgArgs(npz_files=['unused.npz']))
    paper = make_env_cfg(SuperMimicEnvCfgArgs(npz_files=['unused.npz'], paper_protocol=True))
    assert legacy.commands['motion'].anchor_body_name == 'torso_link'
    assert paper.commands['motion'].anchor_body_name == 'pelvis'
    assert legacy.events['base_com'].mode == 'startup'
    assert paper.events['base_com'].mode == 'reset'


def test_full_horizon_summary_does_not_reward_failure():
    rows = [ClipResult('short',100,10,.1,True,10,executed_step_norm_return=1.0),
            ClipResult('long',100,100,1.0,False,-1,executed_step_norm_return=1.0)]
    result = summarize(rows)
    assert result['mean_norm_return'] == pytest.approx(.55)
    assert result['frame_weighted_full_episode_return'] == pytest.approx(.55)


def test_legacy_paths_load_with_restricted_loader(tmp_path):
    path = tmp_path/'legacy.pt'
    torch.save({'config':{'data':{'library':Path('data/library/train.pt')}},
                'policy':{'weight':torch.ones(2)}}, path)
    assert load_checkpoint(path)['config']['data']['library'] == Path('data/library/train.pt')


def test_model_initialization_keeps_training_state_fresh(tmp_path):
    source = {name:torch.nn.Linear(2,1) for name in ('wm','policy','critic')}
    target = SimpleNamespace(device='cpu',iteration=0,num_updates=0,
                             **{name:torch.nn.Linear(2,1) for name in source})
    path = tmp_path/'models.pt'
    torch.save({k:v.state_dict() for k,v in source.items()},path)
    initialize_models(target,path)
    for name in source:
        assert torch.equal(getattr(target,name).weight,source[name].weight)
    assert target.iteration == target.num_updates == 0
    torch.save({'policy':source['policy'].state_dict()},path)
    with pytest.raises(ValueError,match='missing'):
        initialize_models(target,path)


def test_packed_library_uses_clip_count_not_file_count(tmp_path, monkeypatch):
    import supermimic.eval.benchmark as benchmark
    path = tmp_path/'two_clips.pt'
    torch.save({'names':['first','second']},path)
    captured = {}
    class ReachedEnvironment(Exception):
        pass
    def intercept(args, device):
        captured.update(num_envs=args.num_envs,compact=args.compact_library,
                        paper_protocol=args.paper_protocol)
        raise ReachedEnvironment()
    monkeypatch.setattr(benchmark,'make_env',intercept)
    with pytest.raises(ReachedEnvironment):
        benchmark.run_benchmark(None,[str(path)],num_envs=64,paper_protocol=True)
    assert captured == dict(num_envs=2,compact=True,paper_protocol=True)
