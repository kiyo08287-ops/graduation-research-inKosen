import xml.etree.ElementTree as ET
from xml.dom import minidom
import cv2

video = cv2.VideoCapture("/home/yohe_ehoy/VideoPose3D/InputVideo/SampleVideo5.mp4")
fps = video.get(cv2.CAP_PROP_FPS)
frame_num = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# ファイル名の設定
SCALED_MODEL_NAME = "Rajagopal2016_scaled.osim"
MARKER_FILE_NAME = "training_motion.trc"
OUTPUT_MOTION_NAME = "training_motion_ik.mot"

# 計算時間範囲の設定
START_TIME = 0.0
END_TIME = frame_num / fps


# ルート要素の作成
root = ET.Element("OpenSimDocument", Version="40000")

# InverseKinematicsTool要素の作成
ik_tool = ET.SubElement(root, "InverseKinematicsTool", name="InverseKinematics")

# 入力モデルファイル (スケーリング後のモデル)
ET.SubElement(ik_tool, "model_file").text = SCALED_MODEL_NAME

# マーカーファイル (.trc)
ET.SubElement(ik_tool, "marker_file").text = MARKER_FILE_NAME

# 結果の出力ファイル (.mot)
ET.SubElement(ik_tool, "output_motion_file").text = OUTPUT_MOTION_NAME

# 解析時間範囲
ET.SubElement(ik_tool, "time_range").text = f"{START_TIME:.6f} {END_TIME:.6f}"

# マーカーと座標の重み設定 (基本設定)
ik_task_set = ET.SubElement(ik_tool, "IKTaskSet")
objects = ET.SubElement(ik_task_set, "objects")

# TRCファイルで使用しているマーカー名のリストアップ
marker_names = [
    "RHJC", "RKJC", "RAJC", "RCAL", "RTOE",
    "LHJC", "LKJC", "LAJC", "LCAL", "LTOE",
    "RSJC", "REJC", "RFAsuperior", 
    "LSJC", "LEJC", "LFAsuperior", 
    "CLAV", "C7"
]

# この重みを調整してIKの精度を上げる
for name in marker_names:
    weight = "10.0"
    if name in ["RHJC","LHJC"]:
        weight = "30.0"
    if name in ["RAJC","LAJC","RKJC","LKJC"]:
        weight = "40.0"
    if name in ["C7"]:
        weight = "25.0"
    if name in ["CLAV"]:
        weight = "5.0"
    if name in ["RCAL","LCAL","RTOE","LTOE"]:
        weight = "100.0"
    marker_task = ET.SubElement(objects, "IKMarkerTask", name=name)
    ET.SubElement(marker_task, "apply").text = "true"
    ET.SubElement(marker_task, "weight").text = weight

# XMLファイルを整形して保存
xml_str = ET.tostring(root, encoding='utf-8')

dom = minidom.parseString(xml_str)
pretty_xml = dom.toprettyxml(indent="    ")

# ファイルに書き出し
with open("IK_setup.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml.split('\n', 1)[1])

print("IK設定ファイル (IK_setup.xml) の生成が完了しました。")