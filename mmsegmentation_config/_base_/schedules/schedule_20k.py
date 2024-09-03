# optimizer
optimizer = dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0005)
optim_wrapper = dict(type='OptimWrapper', optimizer=optimizer, clip_grad=None)
# learning policy
param_scheduler = [
    dict(
        type='PolyLR',
        eta_min=1e-4,
        power=0.9,
        begin=0,
        end=150,
        by_epoch=True)
]
# training schedule for 150 epochs
# train_cfg = dict(type='IterBasedTrainLoop', max_iters=20000, val_interval=1000)
train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=150, val_interval=5)
# train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=75, val_interval=5)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')
default_hooks = dict(
    # timer=dict(type='IterTimerHook'),
    logger=dict(type='LoggerHook', interval=10, log_metric_by_epoch=True),
    param_scheduler=dict(type='ParamSchedulerHook'),
    checkpoint=dict(type='CheckpointHook', by_epoch=True, interval=10, save_best='mIoU'),
    # checkpoint=dict(type='CheckpointHook', by_epoch=True, interval=1, save_best='mIoU'),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    visualization=dict(type='SegVisualizationHook'))
