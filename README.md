# spec2015_1
***
处理中产生的新文件通过在前面加更多字符来标识
其中 ftbo 分别代表: flat修正,trim,bias修正,overscan
之后的 awftbo 中aw分别代表w(wavelength)波长定标，a(apall)抽谱，以awftbo开头的文件是已经做完波长定标并抽出来的谱
std和sens分别是经过standard和sensfunc命令处理后加的标识，只对标准星进行
mark_开头表示最终抽出来的谱
### 处理流程
* [分类](#分类)
* [生成lst文件](#genlst)
* [检查](#check)
* [分别进入不同目录，正式处理](#proc)


1. <span id='分类'>分类</span>
    1. 将所有的光谱文件移动到一个目录，这里设置该目录名为spec
    2. 根据不同文件名光栅狭缝把fits文件移动到不同目录，目录命名规则Grismname'+"\_"+Slitname，如Grism_8_Slit0.5, Grism_10_Slit5.05，其中bias文件专门建立目录bias
    3. 没有source数据，只有公共数据的目录，移动到other目录
2. <span id='genlst'</span>生成lst文件，分别进入不同目录，生成不同种类fits的lst文件，这些lst文件包括：
    * bias.lst
    * halogen.lst
    * cor_halogen.lst
    * lamp.lst
    * cor_lamp.lst
    * std.lst
    * cor_std.lst
3. <span id='check'>检查</span>
    1. 检查公共文件、standard star文件是否有缺失。若缺失，从临近天拷贝相应数据，重新生成lst文件
    2. 自动检查bias，halogen等文件
    3. 手动检查bias、halogen、lamp、standard、obj，如果有问题，从lst文件中删除
4. <span id='proc'></span>进入不同目录，正式处理
