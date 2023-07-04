import vvcpy as vp

path = '/mnt/c/Users/dudup/OneDrive/Documentos/GitHub/VVC_research/OutputTests'
qps = [22, 27, 32, 37]
cfg = 'AI'
versions = vp.common.commonlib.find_all_versions_in_path(path)
files = vp.common.commonlib.find_all_videos_in_version(path, versions[0])

df = vp.prof.vvc_frame_analysis(versions, files, path, [cfg], qps)
print(df.head(50))
