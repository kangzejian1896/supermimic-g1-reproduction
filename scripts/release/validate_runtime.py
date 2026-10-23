"""Run a tiny real simulation/training loop with a generated, non-dataset motion."""
import argparse,json,tempfile,importlib.util
from pathlib import Path
import torch
from supermimic.config import TrainConfig
from supermimic.training.loop import Trainer
from supermimic.checkpoints import load_checkpoint


def main(models):
    torch.set_num_threads(4)
    root=Path(__file__).resolve().parents[2]
    spec=importlib.util.spec_from_file_location('synthetic',root/'scripts/data/make_synthetic_motion.py')
    synthetic=importlib.util.module_from_spec(spec);spec.loader.exec_module(synthetic)
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp);synthetic.generate(tmp/'npz/stand.npz')
        cfg=TrainConfig(run_name='release_smoke',log_root=tmp/'logs',seed=42)
        cfg.data.npz_dir=tmp/'npz';cfg.env.paper_protocol=True
        cfg.env.num_envs=8;cfg.env.replay_capacity=64
        cfg.wm_trainer.batch_size=16;cfg.wm_trainer.batches_per_update=1;cfg.wm_trainer.window=2;cfg.wm_trainer.compile=None
        cfg.policy_trainer.batch_size=16;cfg.policy_trainer.horizon=4;cfg.policy_trainer.compile=None
        cfg.schedule.total_iterations=20;cfg.schedule.warmup_iterations=10;cfg.schedule.log_interval=10
        cfg.initialize_from=models
        trainer=Trainer(cfg)
        try:
            initial={n:next(getattr(trainer,n).parameters()).detach().clone() for n in ['wm','policy','critic']}
            if models:
                exported=load_checkpoint(models)
                for name in initial:
                    assert all(torch.equal(v.cpu(),exported[name][k]) for k,v in getattr(trainer,name).state_dict().items())
                assert trainer.iteration==trainer.num_updates==0
            trainer.run()
            assert trainer.num_updates>0
            deltas={n:float((next(getattr(trainer,n).parameters()).detach()-initial[n]).abs().max()) for n in initial}
            assert all(x>0 for x in deltas.values()),deltas
            assert all(torch.isfinite(p).all() for n in initial for p in getattr(trainer,n).parameters())
            assert (trainer.log_dir/'ckpt_latest.pt').is_file()
            assert not list(trainer.log_dir.glob('*.tmp'))
            print(json.dumps(dict(real_simulation=True,optimizer_updates=trainer.num_updates,parameter_deltas=deltas,
                                  initialized_from_models=models is not None,atomic_checkpoint=True,
                                  note='Synthetic smoke test; not tracking quality evidence')),flush=True)
        finally:trainer.env.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--models',type=Path);a=p.parse_args();main(a.models)
