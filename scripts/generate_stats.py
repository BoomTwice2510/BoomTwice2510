import os,json,urllib.request,urllib.parse,html
from collections import Counter
U=os.environ["GITHUB_REPOSITORY_OWNER"]; T=os.environ["GITHUB_TOKEN"]
def api(url,method="GET",body=None):
 r=urllib.request.Request(url,data=None if body is None else json.dumps(body).encode(),method=method)
 r.add_header("Authorization","Bearer "+T); r.add_header("Accept","application/vnd.github+json")
 with urllib.request.urlopen(r,timeout=30) as x:return json.loads(x.read())
def esc(x):return html.escape(str(x))
repos=[];p=1
while True:
 x=api(f"https://api.github.com/users/{urllib.parse.quote(U)}/repos?per_page=100&page={p}&type=owner");repos+=x
 if len(x)<100:break
 p+=1
own=[r for r in repos if not r.get("fork")];pub=[r for r in own if not r.get("private")]
langs=Counter()
for r in pub:
 try:langs.update(api(r["languages_url"]))
 except:pass
q="""query($u:String!){user(login:$u){followers contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
g=api("https://api.github.com/graphql","POST",{"query":q,"variables":{"u":U}})["data"]["user"]
cal=g["contributionsCollection"]["contributionCalendar"];total=cal["totalContributions"]
def shell(w,h,t):return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" rx="18" fill="#0b1018"/><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" stroke="#2f4053"/><text x="30" y="42" fill="#f2f6fa" font-family="monospace" font-size="24" font-weight="700">{t}</text>']
def save(n,L):open("assets/"+n,"w").write("\n".join(L+["</svg>"]))
L=shell(900,250,"GITHUB ACTIVITY")
for i,(lab,val,col) in enumerate([("REPOSITORIES",len(own),"#41cdff"),("FOLLOWERS",g["followers"],"#a469ff"),("CONTRIBUTIONS",total,"#55e196"),("STARS",sum(r["stargazers_count"] for r in pub),"#ffa44b")]):
 x=30+i*220
 L.append(f'<rect x="{x}" y="72" width="190" height="135" rx="14" fill="#111a25" stroke="#26384a"/><text x="{x+15}" y="102" fill="#91a0b2" font-family="monospace" font-size="12">{lab}</text><text x="{x+15}" y="155" fill="{col}" font-family="monospace" font-size="30" font-weight="700">{val}</text>')
save("github-stats.svg",L)
top=langs.most_common(6);den=sum(langs.values()) or 1
L=shell(900,300,"TOP LANGUAGES")
for i,(lang,n) in enumerate(top):
 y=78+i*36;pct=n/den*100;col=["#41cdff","#a469ff","#55e196","#ffa44b","#ff5e97","#8be28b"][i]
 L.append(f'<text x="30" y="{y}" fill="#f2f6fa" font-family="monospace" font-size="15">{esc(lang)}</text><text x="830" y="{y}" text-anchor="end" fill="#91a0b2" font-family="monospace" font-size="14">{pct:.1f}%</text><rect x="30" y="{y+13}" width="840" height="8" rx="4" fill="#1b2837"/><rect x="30" y="{y+13}" width="{max(4,840*pct/100)}" height="8" rx="4" fill="{col}"/>')
save("top-languages.svg",L)
L=shell(1200,280,"CONTRIBUTION ACTIVITY");pal=["#152131","#20384a","#2b6873","#35a79c","#55e196"]
for wi,w in enumerate(cal["weeks"][-52:]):
 for ri,d in enumerate(w["contributionDays"]):
  c=d["contributionCount"];lv=0 if c==0 else 1 if c<=2 else 2 if c<=5 else 3 if c<=9 else 4
  L.append(f'<rect x="{30+wi*19}" y="{75+ri*19}" width="15" height="15" rx="3" fill="{pal[lv]}"><title>{d["date"]}: {c} contributions</title></rect>')
L.append(f'<text x="30" y="245" fill="#91a0b2" font-family="monospace" font-size="13">{total} contributions in the displayed year</text>')
save("contributions.svg",L)
