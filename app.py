import json
from pathlib import Path
from datetime import datetime

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

try:
    import tensorflow as tf
except Exception as e:
    tf = None

APP_NAME = "SIP-Ekspresi BK"
APP_SUBTITLE = "Sistem Pengenalan Ekspresi Wajah untuk Pendampingan Bimbingan dan Konseling"

DEFAULT_CLASS_NAMES = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

LABEL_ID = {
    "angry": "Marah",
    "disgust": "Jijik",
    "fear": "Takut/Cemas",
    "happy": "Senang",
    "neutral": "Netral",
    "sad": "Sedih",
    "surprise": "Terkejut",
}

COUNSELING_NOTES = {
    "angry": "Ekspresi marah dapat menjadi sinyal awal untuk membuka percakapan mengenai frustrasi, konflik, atau tekanan yang sedang dirasakan.",
    "disgust": "Ekspresi jijik dapat muncul karena ketidaknyamanan terhadap situasi tertentu. Gunakan sebagai pemantik dialog, bukan kesimpulan.",
    "fear": "Ekspresi takut/cemas perlu ditindaklanjuti secara hati-hati melalui pertanyaan terbuka mengenai rasa aman, kekhawatiran, atau tekanan.",
    "happy": "Ekspresi senang dapat menunjukkan kondisi emosi positif pada saat pengambilan gambar, tetapi tetap perlu dikonfirmasi melalui percakapan.",
    "neutral": "Ekspresi netral belum tentu berarti tidak ada masalah. Hasil ini sebaiknya dibaca bersama konteks wawancara konseling.",
    "sad": "Ekspresi sedih dapat menjadi indikasi awal perlunya eksplorasi lebih lanjut tentang beban emosi, relasi sosial, atau kondisi akademik.",
    "surprise": "Ekspresi terkejut biasanya bersifat sesaat. Interpretasinya sangat bergantung pada konteks sebelum dan saat gambar diambil.",
}

RISK_NOTE = """
Aplikasi ini tidak dimaksudkan untuk diagnosis psikologis, asesmen klinis, atau pengambilan keputusan otomatis terhadap siswa/mahasiswa.
Hasil prediksi hanya merupakan alat bantu observasi awal dan harus dikonfirmasi melalui proses konseling, wawancara, serta pertimbangan profesional.
"""

def _safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

@st.cache_resource
def load_model(model_path: str):
    if tf is None:
        raise RuntimeError("TensorFlow belum terpasang. Jalankan `pip install -r requirements.txt`.")
    return tf.keras.models.load_model(model_path)

def load_class_names(labels_path: Path):
    if labels_path.exists():
        with open(labels_path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        if isinstance(obj, dict) and "class_names" in obj:
            return obj["class_names"]
        if isinstance(obj, list):
            return obj
    return DEFAULT_CLASS_NAMES

def get_face_detector():
    cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    return cv2.CascadeClassifier(str(cascade_path))

def pil_to_rgb_array(img: Image.Image) -> np.ndarray:
    return np.array(img.convert("RGB"))

def detect_faces(rgb_img: np.ndarray, scale_factor=1.1, min_neighbors=5):
    gray = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)
    detector = get_face_detector()
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=(40, 40),
    )
    faces = sorted(faces, key=lambda box: box[2] * box[3], reverse=True)
    return faces, gray

def preprocess_face(gray_img: np.ndarray, face_box, image_size=48):
    x, y, w, h = face_box
    pad = int(0.08 * max(w, h))
    x1 = max(x - pad, 0)
    y1 = max(y - pad, 0)
    x2 = min(x + w + pad, gray_img.shape[1])
    y2 = min(y + h + pad, gray_img.shape[0])

    crop = gray_img[y1:y2, x1:x2]
    resized = cv2.resize(crop, (image_size, image_size), interpolation=cv2.INTER_AREA)
    arr = resized.astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=(0, -1))  # (1, 48, 48, 1)
    return arr, crop

def predict_expression(model, face_arr, class_names):
    probs = model.predict(face_arr, verbose=0)[0]
    idx = int(np.argmax(probs))
    pred_en = class_names[idx]
    pred_id = LABEL_ID.get(pred_en, pred_en)
    conf = float(probs[idx])
    return pred_en, pred_id, conf, probs


def predict_expression_demo(face_arr, class_names):
    """
    Mode demo agar aplikasi tetap dapat dijalankan untuk uji antarmuka/HKI
    sebelum model FER2013 selesai dilatih. Prediksi bersifat heuristik sederhana,
    bukan hasil model ilmiah.
    """
    img = face_arr[0, :, :, 0]
    mean = float(np.mean(img))
    std = float(np.std(img))
    upper = float(np.mean(img[:24, :]))
    lower = float(np.mean(img[24:, :]))

    scores = {c: 0.05 for c in class_names}
    if "neutral" in scores:
        scores["neutral"] += 0.35 + max(0.0, 0.20 - std)
    if "happy" in scores:
        scores["happy"] += max(0.0, lower - upper) * 1.20 + max(0.0, mean - 0.45) * 0.20
    if "sad" in scores:
        scores["sad"] += max(0.0, upper - lower) * 0.90 + max(0.0, 0.45 - mean) * 0.20
    if "surprise" in scores:
        scores["surprise"] += std * 0.70
    if "angry" in scores:
        scores["angry"] += max(0.0, std - 0.18) * 0.55
    if "fear" in scores:
        scores["fear"] += max(0.0, 0.40 - mean) * 0.35 + std * 0.25
    if "disgust" in scores:
        scores["disgust"] += max(0.0, 0.16 - std) * 0.20

    raw = np.array([scores[c] for c in class_names], dtype="float32")
    probs = raw / np.sum(raw)
    idx = int(np.argmax(probs))
    pred_en = class_names[idx]
    pred_id = LABEL_ID.get(pred_en, pred_en)
    conf = float(probs[idx])
    return pred_en, pred_id, conf, probs

def draw_faces(rgb_img: np.ndarray, faces, label_text=None):
    out = rgb_img.copy()
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(out, (x, y), (x + w, y + h), (50, 180, 80), 2)
        if label_text and i == 0:
            cv2.putText(
                out,
                label_text,
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (50, 180, 80),
                2,
                cv2.LINE_AA,
            )
    return out

def init_log():
    if "observation_log" not in st.session_state:
        st.session_state.observation_log = []

def add_log(source, pred_en, pred_id, conf):
    st.session_state.observation_log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "expression_en": pred_en,
        "expression_id": pred_id,
        "confidence": round(conf, 4),
    })

def main():
    st.set_page_config(page_title=APP_NAME, page_icon="🙂", layout="wide")
    init_log()

    st.title(APP_NAME)
    st.caption(APP_SUBTITLE)

    with st.expander("Catatan etika dan batas penggunaan", expanded=True):
        st.warning(RISK_NOTE)
        st.markdown(
            "- Gunakan hanya dengan persetujuan subjek/orang tua/wali bila subjek masih di bawah umur.\n"
            "- Hindari menyimpan foto mentah. Simpan hanya ringkasan observasi bila memang diperlukan.\n"
            "- Jangan gunakan hasil prediksi tunggal sebagai dasar pelabelan kondisi psikologis."
        )

    with st.sidebar:
        st.header("Pengaturan")
        model_path = st.text_input("Path model", value="models/best_fer_model.keras")
        labels_path = Path(st.text_input("Path label", value="models/labels.json"))
        demo_mode = st.checkbox("Izinkan mode demo jika model belum tersedia", value=True)
        input_mode = st.radio("Input gambar", ["Upload gambar", "Ambil foto kamera"], index=0)
        detect_scale = st.slider("Sensitivitas deteksi wajah", 1.05, 1.30, 1.10, 0.05)
        detect_neighbors = st.slider("Min neighbors", 3, 8, 5, 1)
        st.divider()
        st.caption("Versi awal untuk HKI: klasifikasi 7 ekspresi berbasis FER2013 dan Streamlit.")

    model_file = Path(model_path)
    use_demo_predictor = False
    model = None
    if not model_file.exists():
        if demo_mode:
            use_demo_predictor = True
            st.warning(
                f"Model belum ditemukan di `{model_path}`. Aplikasi berjalan dalam MODE DEMO agar antarmuka dapat diuji. "
                "Untuk prediksi sungguhan, jalankan notebook training sampai menghasilkan file model di folder `models/`."
            )
        else:
            st.error(
                f"Model belum ditemukan di `{model_path}`. "
                "Jalankan notebook `01_train_fer2013_streamlit_ready.ipynb` sampai tahap ekspor model, "
                "lalu letakkan file model di folder `models/`."
            )
            st.stop()
    else:
        try:
            model = load_model(str(model_file))
        except Exception as e:
            if demo_mode:
                use_demo_predictor = True
                st.warning("Model tidak dapat dimuat. Aplikasi dialihkan ke MODE DEMO untuk uji antarmuka.")
                st.caption(str(e))
            else:
                st.exception(e)
                st.stop()

    class_names = load_class_names(labels_path)

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    image = None
    source = "upload"

    with col_left:
        st.subheader("1. Masukkan gambar wajah")
        if input_mode == "Upload gambar":
            uploaded = st.file_uploader("Pilih file gambar", type=["jpg", "jpeg", "png", "webp"])
            if uploaded is not None:
                image = Image.open(uploaded)
                source = uploaded.name
        else:
            cam = st.camera_input("Ambil foto")
            if cam is not None:
                image = Image.open(cam)
                source = "camera"

        if image is not None:
            rgb = pil_to_rgb_array(image)
            faces, gray = detect_faces(rgb, scale_factor=detect_scale, min_neighbors=detect_neighbors)

            if len(faces) == 0:
                st.warning("Wajah belum terdeteksi. Coba gunakan gambar yang lebih terang, frontal, dan tidak terlalu jauh.")
                st.image(rgb, caption="Gambar input", use_container_width=True)
            else:
                face_arr, crop = preprocess_face(gray, faces[0])
                if use_demo_predictor:
                    pred_en, pred_id, conf, probs = predict_expression_demo(face_arr, class_names)
                else:
                    pred_en, pred_id, conf, probs = predict_expression(model, face_arr, class_names)
                label_for_box = f"{pred_id} ({conf:.1%})"
                annotated = draw_faces(rgb, faces, label_for_box)
                st.image(annotated, caption="Hasil deteksi wajah dan prediksi ekspresi", use_container_width=True)

                add_log(source, pred_en, pred_id, conf)

                with col_right:
                    st.subheader("2. Hasil observasi")
                    st.metric("Ekspresi dominan", pred_id, f"Confidence {conf:.1%}")
                    if use_demo_predictor:
                        st.warning("Mode demo aktif: hasil hanya untuk demonstrasi aplikasi, bukan prediksi model terlatih.")
                    if conf < 0.50:
                        st.info("Confidence masih rendah. Gunakan hasil ini sebagai sinyal sangat awal dan konfirmasi melalui observasi langsung.")
                    elif conf < 0.70:
                        st.info("Confidence sedang. Interpretasi tetap perlu dikaitkan dengan konteks percakapan.")
                    else:
                        st.success("Confidence relatif tinggi untuk model, namun tetap bukan diagnosis.")

                    prob_df = pd.DataFrame({
                        "Ekspresi": [LABEL_ID.get(c, c) for c in class_names],
                        "Probabilitas": probs.astype(float),
                    }).sort_values("Probabilitas", ascending=False)
                    st.dataframe(prob_df, use_container_width=True, hide_index=True)

                    st.subheader("3. Catatan untuk konselor")
                    st.write(COUNSELING_NOTES.get(pred_en, "Gunakan hasil sebagai bahan refleksi awal dalam proses konseling."))
                    st.caption("Saran: ajukan pertanyaan terbuka, misalnya “Apa yang paling banyak Bapak/Ibu/Saudara rasakan akhir-akhir ini?”")

    st.divider()
    st.subheader("Log observasi sesi ini")
    if st.session_state.observation_log:
        log_df = pd.DataFrame(st.session_state.observation_log)
        st.dataframe(log_df, use_container_width=True, hide_index=True)
        csv = log_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Unduh log CSV",
            data=csv,
            file_name="log_observasi_ekspresi_bk.csv",
            mime="text/csv",
        )
        if st.button("Bersihkan log sesi"):
            st.session_state.observation_log = []
            _safe_rerun()
    else:
        st.caption("Belum ada observasi pada sesi ini.")

if __name__ == "__main__":
    main()