import opensim as osim
import os

# 必要なファイル名を指定
IK_SETUP_FILE = "IK_setup.xml"
OUTPUT_MOTION_NAME = "training_motion_ik.mot"

setup_dir = os.path.abspath(os.path.dirname(IK_SETUP_FILE))

# IK Toolのロードと実行
try:
    ik_tool = osim.InverseKinematicsTool(IK_SETUP_FILE)
    
    print("OpenSim 逆運動学計算実行中...")
    ik_tool.run()
    
    print(f"逆運動学計算が完了しました。結果は {OUTPUT_MOTION_NAME} に出力されました。")

except Exception as e:
    print(f"逆運動学計算中にエラーが発生しました: {e}")