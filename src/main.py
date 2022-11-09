from kma.core import KmaScoreCore

if __name__ == "__main__":
    PATH = "../sample/tong-hop-diem-thi-kthp-hk2-nam-21-22-dot-2-signed.pdf"

    a = KmaScoreCore(PATH)

    a.run()

    print("V2")
