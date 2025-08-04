import matplotlib as mpl
import matplotlib.font_manager as fm
import os

def set_korean_font():
    # 항상 초기화
    mpl.rcParams.update(mpl.rcParamsDefault)

    font_path = None
    if os.name == 'posix':
        # macOS
        mac_font = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
        if os.path.exists(mac_font):
            font_path = mac_font
        # Linux (Streamlit Cloud 포함)
        linux_font = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        if os.path.exists(linux_font):
            font_path = linux_font
    elif os.name == 'nt':  # Windows
        win_font = 'C:/Windows/Fonts/malgun.ttf'
        if os.path.exists(win_font):
            font_path = win_font

    # 폰트 적용
    if font_path and os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        mpl.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
    else:
        mpl.rcParams['font.family'] = 'DejaVu Sans'

    mpl.rcParams['axes.unicode_minus'] = False
