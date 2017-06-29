# spec2015_1
### 流程
* [分类](#1-分类)
* [生成lst文件](#2-生成lst文件)
* [检查](#3-检查)
* [分别进入不同目录，正式处理](#4-进入不同目录正式处理)

#### 1. 分类
  1. 将所有的光谱文件移动到一个目录，这里设置该目录名为spec
  2. 根据不同光栅狭缝把fits文件移动到不同目录，目录命名规则Grismname'+"\_"+Slitname，如Grism_8_Slit0.5, Grism_10_Slit5.05，其中bias文件专门建立目录bias
  3. 没有source数据，只有公共数据的目录，移动到other dir

#### 2. 生成lst文件
分别进入不同目录，生成不同种类fits的lst文件，这些lst文件包括：
>  * bias.lst
>  * halogen.lst
>  * cor_halogen.lst
>  * lamp.lst
>  * cor_lamp.lst
>  * std.lst
>  * cor_std.lst

#### 3. 检查
  1. 检查公共文件、standard star文件是否有缺失。若缺失，从临近天拷贝相应数据，重新生成lst文件
  2. 自动检查bias，halogen等文件
  3. 手动检查bias、halogen、lamp、standard、obj，如有问题，从lst文件中删除

#### 4. 进入不同目录，正式处理
---

### 文件名规范
处理中产生的新文件通过在前面加更多字符来标识。如:
mark_awftbo*.fits
* mark_ 最终的光谱，经过流量定标
* a (apall) 经过抽谱，对应couts谱
* w (wavelength) 经过波长定标
* f (flat) 经过平场改正
* t (trim) 经过裁剪
* b (bias) 经过减bias
* o (overscan) 经过overscan

其他文件有:
* Zero.fits : 合并后的bias
* Halogen.fits : 合并后的平场文件
* Resp.fits : 经过改正后的平场文件
* Lamp.fits : 合并后的定标灯谱文件
* Std : 标准星光谱生成的文件
* Sens.fits : 由标准星光谱生成的响应曲线文件
