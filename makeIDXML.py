import xml.etree.ElementTree as ET
from xml.dom import minidom
import cv2

video = cv2.VideoCapture("/home/yohe_ehoy/VideoPose3D/InputVideo/SampleVideo5.mp4")
fps = video.get(cv2.CAP_PROP_FPS)
frame_num = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# ファイル設定
SCALED_MODEL_NAME = "Rajagopal2016_scaled.osim"
IK_MOTION_NAME = "training_motion_ik.mot"  # IKで作成された運動学データ
OUTPUT_FORCE_NAME = "inverse_dynamics.sto" # IDの結果（関節トルク）が出力されるファイル
EXTERNAL_LOADS_XML = "external_loads.xml"  # 外部荷重（疑似床反力）設定ファイル

# 計算範囲
START_TIME = 0.0
END_TIME = frame_num / fps


# ルート要素の作成
root = ET.Element("OpenSimDocument", Version="40000")

# InverseDynamicsTool要素の作成
id_tool = ET.SubElement(root, "InverseDynamicsTool", name="InverseDynamics")

# 入力モデルファイル (スケーリング後のモデル)
ET.SubElement(id_tool, "model_file").text = SCALED_MODEL_NAME

# 運動学データファイル (.mot)
ET.SubElement(id_tool, "coordinates_file").text = IK_MOTION_NAME

# 結果の出力ファイル (.sto)
ET.SubElement(id_tool, "output_force_file").text = OUTPUT_FORCE_NAME

# 解析時間範囲
ET.SubElement(id_tool, "time_range").text = f"{START_TIME:.6f} {END_TIME:.6f}"

# 力（外力）データの設定
ET.SubElement(id_tool, "external_loads_file").text = EXTERNAL_LOADS_XML 

# ローパスフィルタの設定
ET.SubElement(id_tool, "lowpass_cutoff_frequency_for_coordinates").text = "3.0"

# XMLファイルを整形して保存
xml_str = ET.tostring(root, encoding='utf-8')

dom = minidom.parseString(xml_str)
pretty_xml = dom.toprettyxml(indent="    ")

# ファイルに書き出し
with open("ID_setup.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml.split('\n', 1)[1])

print("ID設定ファイル (ID_setup.xml) の生成が完了しました。")