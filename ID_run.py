import opensim as osim
import os

# 必要なファイル名を指定
ID_SETUP_FILE = "ID_setup.xml"
OUTPUT_FORCE_NAME = "inverse_dynamics.sto"

# ID Toolのロードと実行
try:
    # InverseDynamicsToolのインスタンスを作成
    id_tool = osim.InverseDynamicsTool(ID_SETUP_FILE)
    
    print("OpenSim 逆動力学計算実行中...")
    id_tool.run()
    
    print(f"逆動力学計算が完了しました。結果は {OUTPUT_FORCE_NAME} に出力されました。")

except Exception as e:
    print(f"逆動力学計算中にエラーが発生しました: {e}")