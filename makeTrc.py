import opensim as osim
import EuclidDistance
import numpy as np
import cv2
import math

# 動画ファイルからfpsを取得
video = cv2.VideoCapture("/home/yohe_ehoy/VideoPose3D/InputVideo/SampleVideo5.mp4")
fps = video.get(cv2.CAP_PROP_FPS)

# 設定パラメータ
OUTPUT_TRC_FILE = "training_motion.trc"
FRAME_RATE = fps  # VideoPose3Dが処理した動画のフレームレート (fps) を指定
DATA_RATE = fps   # Frame Rateと同じでOK

# VideoPose3Dの出力の関節名リスト (出力順に一致させる)
JOINT_NAMES_3D = [
    "hip_center", "hip_l", "knee_l", "ankle_l", 
    "hip_r", "knee_r", "ankle_r", "waist", 
    "thorax", "neck", "head", "shoulder_r", 
    "elbow_r", "wrist_r", "shoulder_l", "elbow_l", 
    "wrist_l"
]

# OpenSim IK計算で参照するマーカー名
OPENSIM_MARKER_NAMES = {
    # VideoPose3D関節名:Rajagopal2016モデルマーカー名
    "hip_r": "RHJC",
    "knee_r": "RKJC",
    "ankle_r": "RAJC",
    "hip_l": "LHJC",
    "knee_l": "LKJC",
    "ankle_l": "LAJC",
    "shoulder_r": "RSJC",
    "elbow_r": "REJC",
    "wrist_r": "RFAsuperior",
    "shoulder_l": "LSJC",
    "elbow_l": "LEJC",
    "wrist_l": "LFAsuperior",
    "thorax": "CLAV",
    "neck": "C7",
    # 両踵、両つま先のマーカーを追加
    "RCAL":"RCAL",
    "LCAL":"LCAL",
    "RTOE":"RTOE",
    "LTOE":"LTOE",
}

# OpenSimで使用するマーカー名
marker_header_names = [
    "hip_center", "LHJC", "LKJC", "LAJC", "LCAL", "LTOE",
    "RHJC", "RKJC", "RAJC", "RCAL", "RTOE",
    "waist", "thorax", "neck", "head", 
    "RSJC", "REJC", "RFAsuperior", 
    "LSJC", "LEJC", "LFAsuperior"
]

# 関数: TRCファイルの生成
def generate_trc_file(output_3d_data: np.ndarray, output_filename: str):
    num_frames, num_joints,_  = output_3d_data.shape
    
    num_markers = len(marker_header_names)
    trc_data_rows = []    
    theta = math.radians(300)
    
    for i in range(num_frames):
        frame_num = i + 1
        time = i / FRAME_RATE
        
        row = [str(frame_num), f"{time:.6f}"]

        # 低いほうの足首を地面の高さに固定
        ankle_r_y = -output_3d_data[i,3,1]
        ankle_l_y = -output_3d_data[i,6,1]
        low_ankle_y = min(ankle_r_y,ankle_l_y)
        offset_y = -low_ankle_y+0.07

        # x軸,z軸も足首を固定し他の関節が合わせるように処理
        offset_x = (output_3d_data[i,3,0] + output_3d_data[i,6,0])*0.5
        offset_z = (output_3d_data[i,3,2] + output_3d_data[i,6,2])*0.5

        # 各関節の座標を処理
        coords_dict = {}
        for j in range(num_joints):
            
            x_z = (output_3d_data[i, j, 0] - offset_x)   # 前後
            y = -output_3d_data[i, j, 1]+offset_y        # 高さ
            z_x = (output_3d_data[i, j, 2] - offset_z)   # 左右
            
            # モデルが正面を向くように調整
            x = x_z * math.cos(theta) + z_x * math.sin(theta)
            z = -x_z * math.sin(theta) + z_x * math.cos(theta)

            coords_dict[JOINT_NAMES_3D[j]] = [x,y,z]

        # 踵、つま先のマーカーを追加
        al = coords_dict["ankle_l"]
        coords_dict["LCAL"] = [al[0]-0.05, 0.02,al[2]]
        coords_dict["LTOE"] = [al[0]+0.15, 0.03,al[2]]
        ar = coords_dict["ankle_r"]
        coords_dict["RCAL"] = [ar[0]-0.05, 0.02,ar[2]]
        coords_dict["RTOE"] = [ar[0]+0.15, 0.03,ar[2]]

        name_map = {v: k for k , v in OPENSIM_MARKER_NAMES.items()}

        for name in marker_header_names:
            key = name_map.get(name,name)
            c = coords_dict[key]
            row.extend([f"{c[0]:.6f}",f"{c[1]:.6f}",f"{c[2]:.6f}"])

        trc_data_rows.append('\t'.join(row))

    # TRCヘッダーの作成
    header = [
        f"PathFileType\t4\t(X/Y/Z)\t{output_filename}",
        f"DataRate\tCameraRate\tNumFrames\tNumMarkers\tUnits\tOrigDataRate\tOrigDataStartFrame\tOrigNumFrames",
        f"{DATA_RATE}\t{FRAME_RATE}\t{num_frames}\t{num_markers}\t" + "m" + f"\t{DATA_RATE}\t1\t{num_frames}",
        "Frame#\tTime\t" + '\t'.join(marker_header_names),
        " \t \t" + '\t'.join([f"X{k+1}\tY{k+1}\tZ{k+1}" for k in range(num_markers)])
    ]
    
    # ファイルの書き出し
    with open(output_filename, 'w') as f:
        f.write('\n'.join(header) + '\n')
        f.write('\n'.join(trc_data_rows) + '\n')

    print(f"{output_filename} の生成が完了しました。")
    print(f"フレーム数: {num_frames}, マーカー数: {num_markers}")


# VideoPose3D出力の読み取り
data = np.load("/home/yohe_ehoy/VideoPose3D/Output3Dpose/output3d.npy")

generate_trc_file(data, OUTPUT_TRC_FILE)