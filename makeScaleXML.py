import numpy as np
import xml.etree.ElementTree as ET
from xml.dom import minidom
import EuclidDistance


# スケーリング係数の計算
data_list = np.load("/home/yohe_ehoy/VideoPose3D/Output3Dpose/output3d.npy")
subject_distance_list = EuclidDistance.getDistanceList(data_list)

# AIにRajagopal2016.osimのデフォルトの体節長を求めてもらった
default_length_list = np.array([0.43,0.43,0.55,0.30,0.30,0.25,0.25])

# スケーリング係数([右大腿骨、左大腿骨、体幹(股関節中央-胸郭)、右上腕、左上腕、右前腕、左前腕]はリストの値、ほかは平均値を利用する)
s_list = subject_distance_list / default_length_list
s_ave = np.average(s_list)

print("被験者の体節長：{}\nモデルの体節長：{}\nスケーリング係数：{}\nスケーリング係数(平均)：{}".format(subject_distance_list,default_length_list,s_list,s_ave))

SCALE_FACTORS = {
    "femur_r": s_list[0],
    "femur_l": s_list[1],
    "torso": s_list[2],
    "humerus_r": s_list[3],
    "humerus_l": s_list[4],
    "ulna_r": s_list[5],
    "ulna_l": s_list[6],

    "pelvis": s_ave,
    "tibia_r": s_ave,
    "tibia_l": s_ave,
    "radius_r": s_list[5],
    "radius_l": s_list[6],
    "calcn_r": s_ave,
    "calcn_l": s_ave,
    "talus_r": s_ave,
    "talus_l": s_ave
}

# 被験者の体重
SUBJECT_MASS = 65.0

# ファイルパスの設定
INPUT_MODEL_NAME = "Rajagopal2016.osim"
OUTPUT_MODEL_NAME = "Rajagopal2016_scaled.osim"
OUTPUT_XML_NAME = "scale_tool_setup.xml"

root = ET.Element("OpenSimDocument", Version="40000")

# スケールツールの設定
scale_tool = ET.SubElement(root, "ScaleTool", name="Scaling")
# 入力モデル
ET.SubElement(scale_tool, "model_file").text = INPUT_MODEL_NAME
# 出力モデル
ET.SubElement(scale_tool, "output_model_file").text = OUTPUT_MODEL_NAME
# 被験者の質量（質量スケーリングの入力として使用）
ET.SubElement(scale_tool, "subject_mass").text = str(SUBJECT_MASS)

# Scale Applicationの設定
scale_apps = ET.SubElement(scale_tool, "ScaleTool.Scale_Applications")
scale_app = ET.SubElement(scale_apps, "ScaleApplication", name="subject_scale")
ET.SubElement(scale_app, "apply").text = "true"
# スケーリングは静的姿勢（0秒時点）で一度だけ実行
ET.SubElement(scale_app, "time_range").text = "0.0 0.0" 

# SegmentScaleSetの作成
scale_set = ET.SubElement(scale_app, "SegmentScaleSet")

# 体節ごとのスケーリング係数の適用
for segment_name, factor in SCALE_FACTORS.items():
    segment_scale = ET.SubElement(scale_set, "SegmentScale", name=segment_name)
    scale_text = f"{factor:.4f} {factor:.4f} {factor:.4f}"
    ET.SubElement(segment_scale, "scales").text = scale_text

# マーカー位置合わせ（Marker Placement）のスキップ
marker_placement = ET.SubElement(scale_tool, "ScaleTool.Marker_Placement")
ET.SubElement(marker_placement, "apply").text = "false"

# ET.tostring() でバイト文字列を取得
xml_str = ET.tostring(root, encoding='utf-8')

# minidomで整形
dom = minidom.parseString(xml_str)
pretty_xml = dom.toprettyxml(indent="    ")

# ファイルに書き出し
with open(OUTPUT_XML_NAME, "w", encoding="utf-8") as f:
    f.write(pretty_xml.split('\n', 1)[1])

print(f"{OUTPUT_XML_NAME} の生成が完了しました。")