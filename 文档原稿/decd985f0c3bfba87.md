# CHG-255 修正独立数据库快照导入权限

2026-10-27，基于TEST381实际entrypoint Permission denied，run_trial.py移除initdb目录的0600宿主SQL挂载。保留宿主快照0600，在私有MySQL真正TCP就绪后通过docker exec -i的root客户端stdin导入；不放宽凭据文件权限，不修改原数据库。mysqldump增加--hex-blob以无损文本表示二进制字段。准备后的新输入独立trial-06，不覆盖trial-05或原RAN。

这是数据库副本与权限隔离的工程修正，3GPP/新增数学推导不适用。5QI/QFI的通信依据、业务参数和成功门槛保持CHG254及变更依据与验证路径.md，原文已核16份可读无缺件。命令和实际结果见TEST382；Git取消。
