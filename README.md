# 人类基因组知识地图 / Human Genome Atlas

**[在线页面源码](index.html)** — 下载 HTML 后可离线打开。公开网页可在 GitHub 仓库 Settings → Pages → Deploy from a branch → main / root 启用。

## 已提交
- [交互式知识地图](index.html)：25 条参考序列、9 个主题、19 个教学基因案例、官方 GTF 导入与 FASTA+FAI 局部读取。
- [固定官方来源与 MD5](data/catalog.json)：T2T-CHM13v2.0、UCSC hs1、GCA_009914755.4。
- [校验脚本](scripts/verify_data.py)：数据 MD5、全部 FASTA 序列长度、25 条序列总长度、GTF 格式、SHA256 来源记录。
- [手动触发镜像工作流](.github/workflows/mirror-genome.yml)：下载约 930 MB FASTA、染色体长度表与约 37 MB RefSeq GTF，并在通过验证后创建 Release。

## 下载完整官方数据
打开 **Actions → Mirror pinned T2T-CHM13v2.0 reference → Run workflow**，工作流执行成功后到 [Releases](../../releases) 下载。工作流绝不覆盖同名 Release。

**注意：仓库中的工作流配置与真正的大型 DNA 镜像是两回事。未见 Release 和完整性验证结果之前，不宣称镜像已经完成。**

## 来源
- [UCSC hs1 参考数据目录](https://hgdownload.soe.ucsc.edu/goldenPath/hs1/bigZips/)
- [T2T Consortium](https://github.com/marbl/CHM13)
- [NCBI GCA_009914755.4](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_009914755.4/)
- [HPRC 泛基因组](https://www.humanpangenome.org/data/)（只提供官方链接，未镜像）

本知识地图以可核查的参考基因组坐标为底座；它不是一个人的完整二倍体基因组，也不是所有 DNA 功能均被破解的证明。此科普内容不提供个人医疗诊断。