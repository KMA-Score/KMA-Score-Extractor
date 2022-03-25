# KMA Score Extractor
Đây là công cụ giúp nhận dạng và phân loại điểm theo từng môn từ file PDF từ phòng khảo thí Học viện Kỹ thuật mật mã.
> Công cụ chỉ hoạt động với một định dạng PDF cụ thể.
## Mục lục
- [Giới thiệu chung](https://github.com/Haven-Code/KMA-Score-Extractor/blob/phuchptty-patch-1/README.md#gi%E1%BB%9Bi-thi%E1%BB%87u-chung)
- [Công nghệ sử dụng](https://github.com/Haven-Code/KMA-Score-Extractor/blob/phuchptty-patch-1/README.md#c%C3%A0i-%C4%91%E1%BA%B7t-m%C3%B4i-tr%C6%B0%E1%BB%9Dng)
- [Cài đặt môi trường](https://github.com/Haven-Code/KMA-Score-Extractor/blob/phuchptty-patch-1/README.md#c%C3%A0i-%C4%91%E1%BA%B7t-m%C3%B4i-tr%C6%B0%E1%BB%9Dng)
- [Chạy ứng dụng](https://github.com/Haven-Code/KMA-Score-Extractor/blob/phuchptty-patch-1/README.md#ch%E1%BA%A1y-%E1%BB%A9ng-d%E1%BB%A5ng)
- [Giấy phép](https://github.com/Haven-Code/KMA-Score-Extractor/blob/phuchptty-patch-1/README.md#gi%E1%BA%A5y-ph%C3%A9p)
- [Ủng hộ](https://github.com/Haven-Code/KMA-Score-Extractor/blob/phuchptty-patch-1/README.md#%E1%BB%A7ng-h%E1%BB%99)
## Giới thiệu chung
Dự án được sinh ra nhằm mục đích phục vụ nghiên cứu đồng thời bổ sung tính năng tra cứu điểm cho ứng dụng [iKMA](https://kma.dhpgo.com). Với vai trò là lựa chọn thay thế bên cạnh bảng điểm tại trang QLĐT.
## Công nghệ sử dụng
Dự án sử dụng công nghệ: 
- Xử lý hình ảnh (OpenCV)
- Nhận diện ký tự quang học (OCR) sử dụng thư viện [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- Database: Sqlite3
- Ngôn ngữ sử dụng: Python 3.9
## Cài đặt môi trường
### Bước 1: Cài đặt PyTorch
Pytorch đưa ra 2 lựa chọn: sử dụng GPU và sử dụng CPU. GPU sẽ cho ra hiệu năng cao hơn nhưng yêu cầu máy tính phải có GPU Nvidia (không tính các dòng GPU Mobile).

#### Sử dụng GPU
- Tải xuống và cài đặt CUDA toolkit [tại đây](https://developer.nvidia.com/cuda-downloads).
- Cài đặt [Pytorch](https://pytorch.org/get-started/locally/) có hỗ trợ GPU
```shell
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
```
#### Sử dụng CPU
```shell
pip3 install torch torchvision torchaudio
```
### Bước 2: Cài đặt các gói phụ trợ
- [Pdf2image] Theo hướng dẫn [tại đây](https://github.com/Belval/pdf2image#how-to-install) để cài đặt các gói bổ trợ `Poppler` (Windows & Mac) hoặc `pdftoppm` và `pdftocairo` (Linux).
- [Camelot] Yêu cầu Ghostscipt và Tkinter
#### Ubuntu
```
$ apt install ghostscript python3-tk
```

#### MacOS
```
$ brew install ghostscript tcl-tk
```

#### Windows
Tải xuống và cài đặt phiên bản cho Windows [tại trang của họ](https://ghostscript.com/releases/gsdnld.html). Sau đó thêm đường dẫn đến thư mục `bin` vào PATH
Ví dụ: `C:\Program Files\gs\gs9.55.0\bin`
### Bước 3: Cài đặt thư viện Python
```
pip3 install opencv-python opencv-python-headless==4.5.1.48 tqdm matplotlib numpy
pip3 install camelot-py[cv] pdf2image easyocr
```

## Chạy ứng dụng
Tham khảo 2 file [main.py](https://github.com/Haven-Code/KMA-Score-Extractor/blob/main/src/main.py) và [export_sql.py](https://github.com/Haven-Code/KMA-Score-Extractor/blob/main/src/export_sql.py) trong thư mục `src`
## Giấy phép
Phần mềm được phát hành dưới [giấy phép MIT](https://github.com/Haven-Code/KMA-Score-Extractor/blob/main/LICENSE). Tìm hiểu thêm về giấy phép này [tại đây](https://viblo.asia/p/tim-hieu-cach-hoat-dong-cua-cac-loai-license-ma-nguon-mo-open-source-license-GrLZDknOKk0#_d-mit-license-7).
## Ủng hộ
- [Paypal](https://paypal.me/phuchptty)
- [Momo](https://nhantien.momo.vn/Gjs532xiR34)
- [Buy Me A Coffee](https://www.buymeacoffee.com/phuchptty)
- 9500101239007 - MB Bank - Đặng Hoàng Phúc
