import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Cấu hình giao diện trang web
st.set_page_config(page_title="Quản Lý Điểm Sinh Viên", page_icon="📊", layout="wide")

# 1. Hiển thị tiêu đề
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# Khởi tạo dữ liệu 10 sinh viên
data = {
    'Ho_va_ten': [
        'Nguyễn Văn An',
        'Trần Thị Bình',
        'Lê Hoàng Cường',
        'Phạm Thị Dung',
        'Hoàng Văn Em',
        'Vũ Thị Phương',
        'Đỗ Minh Giang',
        'Bùi Thị Hoa',
        'Ngô Quang Huy',
        'Đinh Thị Khanh',
    ],
    'Chuyen_can': [8.0, 9.0, 7.5, 6.0, 8.5, 9.5, 4.5, 7.0, 8.0, 5.5],
    'Giua_ky': [7.5, 8.5, 6.5, 5.5, 8.0, 9.0, 4.0, 6.5, 7.5, 5.0],
    'Cuoi_ky': [8.0, 8.5, 7.0, 5.0, 8.5, 9.0, 3.5, 6.5, 7.5, 4.5],
}

df = pd.DataFrame(data)

# Tính điểm tổng kết
df['Tong_ket'] = (
    0.2 * df['Chuyen_can'] + 0.3 * df['Giua_ky'] + 0.5 * df['Cuoi_ky']
).round(2)


# Hàm xếp loại sinh viên
def phan_loai(diem):
  if diem >= 8.5:
    return 'Giỏi'
  elif diem >= 7.0:
    return 'Khá'
  elif diem >= 5.0:
    return 'Trung bình'
  else:
    return 'Yếu'


df['Xep_loai'] = df['Tong_ket'].apply(phan_loai)

# 2. Hiển thị bảng điểm đầy đủ
st.subheader("📋 Bảng điểm tổng hợp của sinh viên")
st.dataframe(df, use_container_width=True)

# 3. Thống kê lớp học
diem_tb_lop = df['Tong_ket'].mean()
max_score = df['Tong_ket'].max()
min_score = df['Tong_ket'].min()

sv_max = df[df['Tong_ket'] == max_score]
sv_min = df[df['Tong_ket'] == min_score]
so_sv_dat = len(df[df['Tong_ket'] >= 5.0])

st.subheader("📈 Thống kê lớp học")
col1, col2, col3 = st.columns(3)
col1.metric("Điểm trung bình của lớp", f"{diem_tb_lop:.2f}")
col2.metric("Số sinh viên đạt (>= 5.0)", f"{so_sv_dat} / {len(df)}")
col3.metric("Tỷ lệ đạt", f"{(so_sv_dat / len(df)) * 100:.1f}%")

st.markdown(
    f"🏆 **Sinh viên có điểm cao nhất:** {', '.join(sv_max['Ho_va_ten'])} (Điểm:"
    f" {max_score})"
)
st.markdown(
    f"⚠️ **Sinh viên có điểm thấp nhất:** {', '.join(sv_min['Ho_va_ten'])} (Điểm:"
    f" {min_score})"
)
st.markdown("---")

# 4. Danh sách xổ xuống tra cứu sinh viên
st.subheader("🔍 Tra cứu thông tin cá nhân sinh viên")
selected_student = st.selectbox(
    "Chọn tên sinh viên cần xem chi tiết:", df["Ho_va_ten"]
)

student_info = df[df["Ho_va_ten"] == selected_student].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Điểm Chuyên Cần", student_info["Chuyen_can"])
c2.metric("Điểm Giữa Kỳ", student_info["Giua_ky"])
c3.metric("Điểm Cuối Kỳ", student_info["Cuoi_ky"])
c4.metric("Điểm Tổng Kết", student_info["Tong_ket"])
c5.metric("Xếp Loại", student_info["Xep_loai"])

st.markdown("---")

# 5. Biểu đồ cột tổng kết
st.subheader("📊 Biểu đồ cột điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(
    df["Ho_va_ten"],
    df["Tong_ket"],
    color="#4C72B0",
    edgecolor="#2C3E50",
    width=0.6,
)
ax.set_title(
    "Biểu đồ điểm tổng kết lớp học", fontsize=14, fontweight="bold", pad=15
)
ax.set_xlabel("Họ và tên sinh viên", fontsize=12, fontweight="bold")
ax.set_ylabel("Điểm tổng kết", fontsize=12, fontweight="bold")
plt.xticks(rotation=45, ha="right", fontsize=10)
ax.set_ylim(0, 10)
ax.grid(axis="y", linestyle="--", alpha=0.6)

for bar in bars:
  height = bar.get_height()
  ax.text(
      bar.get_x() + bar.get_width() / 2.0,
      height + 0.1,
      f"{height:.1f}",
      ha="center",
      va="bottom",
      fontsize=9,
      fontweight="bold",
  )

plt.tight_layout()
st.pyplot(fig)

# 6. Thông tin người tạo ở cuối trang (Hãy sửa lại Họ tên và MSSV của bạn vào đây)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>Người tạo"
    " ứng dụng: [Họ và Tên của bạn] - MSSV: [Mã số sinh viên của bạn]</p>",
    unsafe_allow_html=True,
)