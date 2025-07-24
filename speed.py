from flask import Flask, Response, stream_with_context
import requests

app = Flask(__name__)

# ✅ Cookie and headers
COOKIE = {
    "browserid": "ilDpDmPAFb8DySjrTjND8iFOyhX0IU4DsrezKfKDEhGhHL-BHin1_QiQHxU=",
    "lang": "en",
    "ndus": "YQ4ULd1peHuizmwLAoq8OsZ6_JvGlqwK5N2poeSY",
    "PANWEB": "1",
    "__bid_n": "1983cb2fa8946d02f64207"
}

DL_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://dm.1024terabox.com/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# ✅ Final direct TeraBox link
FINAL_DIRECT_LINK = "https://data.1024terabox.com/file/306aa9750e3d583fe9d73033de236727?bkt=en-1df98aeb722e81f5d75d4afa30333f1ef9c339452310d4052b4480855d0085f0f352f64605f97a47&xcode=e4a5e686a7588a8d86a366e972119a8a9b04c8673885a9a98c5d357ef894c5793ca74742898d5e2c7188a49f5180c162e801268afdb15995&fid=81366939570547-250528-1072014057053710&time=1753398202&sign=FDTAXUGERLQlBHSKfWapon-DCb740ccc5511e5e8fedcff06b081203-0LZbymjgxSKMiYskKMdyjYRPsXU%3D&to=171&size=1476033313&sta_dx=1476033313&sta_cs=13&sta_ft=mp4&sta_ct=5&sta_mt=0&fm2=MH%2Ctky%2CAnywhere%2C%2CSmhhcmtoYW5k%2Cany&region=tky&ctime=1750394958&mtime=1753389370&resv0=-1&resv1=0&resv2=&resv3=&resv4=1476033313&vuk=81366939570547&iv=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-036fc523eda33448062c813b3c67a1fbb14ac852358d7a47bacebb4abbcfccc1e4d4a24b15fc445e&sl=79757390&expires=1753427002&rt=pr&r=678483340&vbdid=-&fin=BY25.mp4&fn=BY25.mp4&rtype=1&dp-logid=149661076961934110&dp-callid=0.1&hps=1&tsl=30&csl=30&fsl=-1&csign=6DaeauQjsLtgPAfJH3s9RJwmvxI%3D&so=0&ut=6&uter=4&serv=1&uc=2566351445&ti=9c74a385a1d3afc5f4d6c870a21f2595d34c1ae3569d3d4f305a5e1275657320&tuse=1&raw_appid=0&ogr=0&rregion=XVVi&adg=&reqlabel=250528_f_22057316deeed71984c62ee2fd7fb17d_-1_cb647ff157d37bb2a9e6998361cc15e6&ccn=IN&by=themis"

@app.route("/download")
def download_file():
    filename = "BY25.mp4"

    try:
        remote = requests.get(
            FINAL_DIRECT_LINK,
            headers=DL_HEADERS,
            cookies=COOKIE,
            stream=True,
            allow_redirects=True
        )

        if not remote.ok and remote.status_code != 206:
            return f"❌ Download failed: {remote.status_code}", remote.status_code

        def generate():
            for chunk in remote.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk

        response_headers = {
            "Content-Type": remote.headers.get("Content-Type", "application/octet-stream"),
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Accept-Ranges": "bytes",
            "Cache-Control": "no-store"
        }

        # Forward important headers like content length/range
        for h in ["Content-Length", "Content-Range"]:
            if h in remote.headers:
                response_headers[h] = remote.headers[h]

        return Response(stream_with_context(generate()), headers=response_headers, status=remote.status_code)

    except Exception as e:
        return f"❌ Error: {str(e)}", 500

# ✅ Run on all interfaces
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
