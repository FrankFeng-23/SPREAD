_base_ = [
    '../_base_/models/lraspp_m-v3-d8.py', '../_base_/datasets/pretrained_dataset.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_20k.py'
]
crop_size = (512, 512)
data_preprocessor = dict(size=crop_size)
model = dict(
    data_preprocessor=data_preprocessor,
    pretrained='open-mmlab://contrib/mobilenet_v3_large')

# Re-config the data sampler.
train_dataloader = dict(batch_size=8, num_workers=8)
val_dataloader = dict(batch_size=1, num_workers=8)
test_dataloader = val_dataloader

runner = dict(type='EpochBasedRunner', max_epochs=75)
