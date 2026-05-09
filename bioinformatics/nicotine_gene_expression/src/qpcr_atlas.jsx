import { useState } from "react";

const GENES = ["INSRR","IGF2","CCL2","PAIPB","SLC27A6","BCAS1\u2605","MOBP\u2605","MBP","COL1A1","CDH19","ERNM","OPALIN","FGF1"];
const JITTER = [-26,-16,-6,4,14,24,-20,-2,18];

const CTRL = [
  {id:"C1",  out:false, INSRR:0.5546,IGF2:0.4689,CCL2:0.9450,PAIPB:0.4416,SLC27A6:0.9029,"BCAS1\u2605":0.4836,"MOBP\u2605":0.5171,MBP:0.6419,COL1A1:0.4894,CDH19:0.3799,ERNM:1.3866,OPALIN:0.7608,FGF1:0.5400},
  {id:"C2",  out:false, INSRR:0.8709,IGF2:0.9697,CCL2:0.5160,PAIPB:0.6983,SLC27A6:1.0695,"BCAS1\u2605":0.4732,"MOBP\u2605":0.3726,MBP:0.4796,COL1A1:1.0143,CDH19:0.5864,ERNM:1.0693,OPALIN:0.7344,FGF1:0.7314},
  {id:"C3",  out:false, INSRR:0.4098,IGF2:0.7156,CCL2:0.6307,PAIPB:0.7425,SLC27A6:0.8805,"BCAS1\u2605":0.7325,"MOBP\u2605":0.8569,MBP:1.0411,COL1A1:0.8546,CDH19:0.6087,ERNM:3.0767,OPALIN:1.2207,FGF1:0.7262},
  {id:"C5",  out:false, INSRR:0.5617,IGF2:0.6330,CCL2:0.4403,PAIPB:0.9074,SLC27A6:1.0162,"BCAS1\u2605":0.9807,"MOBP\u2605":0.9120,MBP:1.1352,COL1A1:1.0972,CDH19:0.9570,ERNM:3.0682,OPALIN:1.2873,FGF1:1.3326},
  {id:"C6\u26a0",out:true, INSRR:0.2708,IGF2:0.3856,CCL2:1.5174,PAIPB:0.8589,SLC27A6:1.0730,"BCAS1\u2605":1.9568,"MOBP\u2605":0.5418,MBP:3.0910,COL1A1:0.9953,CDH19:1.1906,ERNM:6.2386,OPALIN:1.1173,FGF1:2.7066},
  {id:"C7",  out:false, INSRR:0.7752,IGF2:0.6577,CCL2:0.7525,PAIPB:1.0047,SLC27A6:1.0022,"BCAS1\u2605":0.9374,"MOBP\u2605":0.6237,MBP:1.1639,COL1A1:1.1298,CDH19:0.7383,ERNM:1.7220,OPALIN:1.1685,FGF1:1.1198},
  {id:"C10", out:false, INSRR:0.9806,IGF2:0.9047,CCL2:0.9782,PAIPB:0.7219,SLC27A6:1.3076,"BCAS1\u2605":0.8639,"MOBP\u2605":1.0812,MBP:1.1644,COL1A1:1.2048,CDH19:0.8729,ERNM:2.7316,OPALIN:1.3998,FGF1:0.9257},
  {id:"C11", out:false, INSRR:1.1151,IGF2:0.8650,CCL2:0.5460,PAIPB:0.7649,SLC27A6:0.8855,"BCAS1\u2605":0.6224,"MOBP\u2605":0.4652,MBP:0.9629,COL1A1:1.1332,CDH19:0.6771,ERNM:1.5213,OPALIN:0.9870,FGF1:0.8551},
  {id:"C12", out:false, INSRR:0.6655,IGF2:0.7671,CCL2:0.6712,PAIPB:0.7033,SLC27A6:1.0603,"BCAS1\u2605":0.8142,"MOBP\u2605":0.9909,MBP:1.1151,COL1A1:1.6282,CDH19:0.7243,ERNM:2.4203,OPALIN:0.8257,FGF1:0.9919},
];

const VDS = [
  {id:"V1",  INSRR:1.4947,IGF2:1.4060,CCL2:0.9472,PAIPB:0.9289,SLC27A6:1.1914,"BCAS1\u2605":0.8378,"MOBP\u2605":0.7151,MBP:0.9876,COL1A1:1.6644,CDH19:0.7391,ERNM:1.8170,OPALIN:0.9471,FGF1:1.0656},
  {id:"V2",  INSRR:1.3906,IGF2:1.0124,CCL2:1.2014,PAIPB:0.8817,SLC27A6:0.7821,"BCAS1\u2605":0.4223,"MOBP\u2605":0.2668,MBP:0.4956,COL1A1:1.0673,CDH19:0.5639,ERNM:1.0730,OPALIN:0.7694,FGF1:1.0040},
  {id:"V3",  INSRR:1.1511,IGF2:1.3089,CCL2:0.9368,PAIPB:1.2448,SLC27A6:1.4887,"BCAS1\u2605":0.7045,"MOBP\u2605":0.5326,MBP:0.5787,COL1A1:1.4001,CDH19:0.8221,ERNM:1.4159,OPALIN:0.7123,FGF1:1.2544},
  {id:"V4",  INSRR:0.7452,IGF2:0.6736,CCL2:0.8437,PAIPB:0.7175,SLC27A6:0.7434,"BCAS1\u2605":0.7203,"MOBP\u2605":0.4784,MBP:0.8305,COL1A1:0.8866,CDH19:0.5968,ERNM:1.9384,OPALIN:1.1565,FGF1:0.8652},
  {id:"V5",  INSRR:0.8140,IGF2:0.7281,CCL2:0.7566,PAIPB:0.8589,SLC27A6:1.0940,"BCAS1\u2605":0.5834,"MOBP\u2605":0.2978,MBP:0.7259,COL1A1:0.7154,CDH19:0.5459,ERNM:1.7295,OPALIN:0.9420,FGF1:0.8904},
  {id:"V7",  INSRR:1.4044,IGF2:1.2506,CCL2:0.7412,PAIPB:0.8506,SLC27A6:0.9228,"BCAS1\u2605":0.5162,"MOBP\u2605":0.3213,MBP:0.5466,COL1A1:1.5414,CDH19:0.6473,ERNM:0.8615,OPALIN:0.6504,FGF1:0.9611},
  {id:"V8",  INSRR:0.6347,IGF2:0.7772,CCL2:0.5767,PAIPB:0.9962,SLC27A6:0.1986,"BCAS1\u2605":0.9416,"MOBP\u2605":0.7408,MBP:1.2258,COL1A1:0.7149,CDH19:0.7548,ERNM:1.9748,OPALIN:1.6414,FGF1:1.1035},
  {id:"V10", INSRR:0.6981,IGF2:1.0405,CCL2:1.5086,PAIPB:1.1253,SLC27A6:1.2732,"BCAS1\u2605":1.3859,"MOBP\u2605":0.9546,MBP:1.6203,COL1A1:1.1168,CDH19:0.6197,ERNM:3.0132,OPALIN:1.5869,FGF1:1.6691},
  {id:"V12", INSRR:0.6158,IGF2:0.6906,CCL2:0.9655,PAIPB:1.0165,SLC27A6:0.8712,"BCAS1\u2605":1.0054,"MOBP\u2605":0.4061,MBP:0.7403,COL1A1:0.7101,CDH19:0.6674,ERNM:2.0240,OPALIN:0.9948,FGF1:1.2248},
];

function foldColor(v) {
  const val = Math.min(Math.max(v, 0), 7);
  if (val <= 1.0) {
    const t = val;
    return `rgb(${Math.round(18+t*227)},${Math.round(58+t*187)},${Math.round(178+t*72)})`;
  }
  const t = Math.min((val - 1) / 6, 1);
  return `rgb(${Math.round(245-t*45)},${Math.round(245-t*215)},${Math.round(250-t*220)})`;
}
function txtCol(v) { return (v < 0.62 || v > 2.1) ? '#fff' : '#091520'; }
function gmean(arr, g) { return arr.reduce((s, r) => s + (r[g] || 0), 0) / arr.length; }
function gsd(arr, g) {
  const m = gmean(arr, g);
  return Math.sqrt(arr.reduce((s, r) => s + ((r[g] || 0) - m) ** 2, 0) / (arr.length - 1));
}

const ACCENT = '#00c8a8', DIM = '#3a6070', BG = '#060e18', CBLUE = '#3a8ae0', VCORAL = '#ff6848';
const LW=90, CW=36, CH=24, HH=72, SEP=14, RP=22;
const svgW = LW + 9*CW + SEP + 9*CW + RP + 56;
const svgH = HH + GENES.length*CH + 56;

export default function App() {
  const [tab, setTab] = useState('heatmap');
  const [selG, setSelG] = useState('ERNM');
  const [tt, setTt] = useState(null);
  const [mx, setMx] = useState(0);
  const [my, setMy] = useState(0);

  return (
    <div style={{background:BG,minHeight:'100vh',fontFamily:"'Courier New',Courier,monospace",color:'#98bcd0',userSelect:'none'}}
         onMouseMove={e=>{setMx(e.clientX);setMy(e.clientY);}}>

      {/* HEADER */}
      <div style={{padding:'20px 28px 14px',borderBottom:'1px solid #0e2535',display:'flex',alignItems:'baseline',gap:20}}>
        <div>
          <div style={{fontSize:17,color:ACCENT,letterSpacing:4,fontWeight:'bold'}}>qPCR EXPRESSION ATLAS</div>
          <div style={{fontSize:9.5,color:DIM,letterSpacing:2.5,marginTop:4}}>
            7 PLATES · 13 TARGETS · GAPDH-NORMALIZED · CTRL n=9 · VDS n=9 · ★ = CORRECTED CURVE
          </div>
        </div>
        <div style={{marginLeft:'auto',display:'flex',gap:8}}>
          {[['heatmap','HEATMAP'],['dist','DISTRIBUTIONS'],['qc','QC FLAGS \u26a0']].map(([k,l])=>(
            <button key={k} onClick={()=>setTab(k)}
              style={{padding:'7px 16px',background:tab===k?'#0a1d2e':'transparent',
                color:tab===k?ACCENT:DIM,border:`1px solid ${tab===k?'#1a4060':'#0e2535'}`,
                borderRadius:3,fontSize:9,letterSpacing:1.5,cursor:'pointer',outline:'none'}}>
              {l}
            </button>
          ))}
        </div>
      </div>

      <div style={{padding:'20px 28px'}}>

        {/* ═══ HEATMAP ═══ */}
        {tab==='heatmap' && (
          <div>
            <div style={{fontSize:9,color:DIM,letterSpacing:1.5,marginBottom:12}}>
              FOLD CHANGE RELATIVE TO GAPDH-NORMALIZED STANDARD · HOVER CELLS FOR VALUES
            </div>
            <div style={{overflowX:'auto'}}>
              <svg width={svgW} height={svgH} onMouseLeave={()=>setTt(null)}>

                {/* Group banners */}
                <text x={LW+9*CW/2} y={14} textAnchor="middle" fill={CBLUE} fontSize={8.5} letterSpacing={2}>CONTROLS</text>
                <line x1={LW+3} y1={19} x2={LW+9*CW-3} y2={19} stroke={CBLUE} strokeWidth={0.6} opacity={0.4}/>
                <text x={LW+9*CW+SEP+9*CW/2} y={14} textAnchor="middle" fill={VCORAL} fontSize={8.5} letterSpacing={2}>VDS</text>
                <line x1={LW+9*CW+SEP+3} y1={19} x2={LW+9*CW+SEP+9*CW-3} y2={19} stroke={VCORAL} strokeWidth={0.6} opacity={0.4}/>

                {/* Sample headers */}
                {CTRL.map((s,ci)=>(
                  <text key={s.id} x={LW+ci*CW+CW/2} y={22} textAnchor="start"
                    fill={s.out?'#ffaa44':CBLUE} fontSize={8}
                    transform={`rotate(-58,${LW+ci*CW+CW/2},22)`}>{s.id}</text>
                ))}
                {VDS.map((s,vi)=>(
                  <text key={s.id} x={LW+9*CW+SEP+vi*CW+CW/2} y={22} textAnchor="start"
                    fill={VCORAL} fontSize={8}
                    transform={`rotate(-58,${LW+9*CW+SEP+vi*CW+CW/2},22)`}>{s.id}</text>
                ))}
                <text x={LW+9*CW+SEP+9*CW+RP+20} y={HH-6} textAnchor="middle" fill={DIM} fontSize={7.5} letterSpacing={0.5}>V/C</text>

                {/* Gene rows */}
                {GENES.map((g,gi)=>{
                  const y = HH + gi*CH;
                  const cM = gmean(CTRL,g), vM = gmean(VDS,g);
                  const ratio = vM/cM;
                  const rc = ratio>1.25?'#ff8855':ratio<0.80?'#5599ee':'#3a6070';
                  return (
                    <g key={g}>
                      <text x={LW-6} y={y+CH/2+3.5} textAnchor="end"
                        fill={g.includes('\u2605')?ACCENT:'#7898b8'} fontSize={9.5}>
                        {g}
                      </text>

                      {/* Ctrl cells */}
                      {CTRL.map((s,ci)=>{
                        const val=s[g]||0, bg=foldColor(val), tc=txtCol(val);
                        const cx=LW+ci*CW;
                        return (
                          <g key={s.id} style={{cursor:'crosshair'}}
                            onMouseEnter={()=>setTt({sample:s.id,gene:g,val,type:'CTRL',out:s.out})}
                            onMouseLeave={()=>setTt(null)}>
                            <rect x={cx+0.5} y={y+0.5} width={CW-1} height={CH-1} fill={bg} rx={1}/>
                            {s.out&&<rect x={cx+0.5} y={y+0.5} width={CW-1} height={CH-1} fill="none" stroke="#ffaa44" strokeWidth={1.2} rx={1}/>}
                            <text x={cx+CW/2} y={y+CH/2+3} textAnchor="middle" fill={tc} fontSize={7.5}>{val.toFixed(2)}</text>
                          </g>
                        );
                      })}

                      {/* VDS cells */}
                      {VDS.map((s,vi)=>{
                        const val=s[g]||0, bg=foldColor(val), tc=txtCol(val);
                        const cx=LW+9*CW+SEP+vi*CW;
                        return (
                          <g key={s.id} style={{cursor:'crosshair'}}
                            onMouseEnter={()=>setTt({sample:s.id,gene:g,val,type:'VDS'})}
                            onMouseLeave={()=>setTt(null)}>
                            <rect x={cx+0.5} y={y+0.5} width={CW-1} height={CH-1} fill={bg} rx={1}/>
                            <text x={cx+CW/2} y={y+CH/2+3} textAnchor="middle" fill={tc} fontSize={7.5}>{val.toFixed(2)}</text>
                          </g>
                        );
                      })}

                      {/* Ratio badge */}
                      <text x={LW+9*CW+SEP+9*CW+RP+20} y={y+CH/2+3.5} textAnchor="middle"
                        fill={rc} fontSize={9} fontWeight="bold">{ratio.toFixed(2)}x</text>

                      <line x1={LW} y1={y+CH} x2={LW+9*CW+SEP+9*CW} y2={y+CH} stroke="#0c2030" strokeWidth={0.5}/>
                    </g>
                  );
                })}

                {/* Vertical grid */}
                {[...Array(10)].map((_,i)=>(
                  <line key={`cg${i}`} x1={LW+i*CW} y1={HH} x2={LW+i*CW} y2={HH+GENES.length*CH} stroke="#0c2030" strokeWidth={0.5}/>
                ))}
                {[...Array(10)].map((_,i)=>(
                  <line key={`vg${i}`} x1={LW+9*CW+SEP+i*CW} y1={HH} x2={LW+9*CW+SEP+i*CW} y2={HH+GENES.length*CH} stroke="#0c2030" strokeWidth={0.5}/>
                ))}

                {/* Legend */}
                {(()=>{
                  const lx=LW, ly=HH+GENES.length*CH+16, lw=200, lh=10;
                  return (
                    <g>
                      <text x={lx} y={ly-3} fill={DIM} fontSize={7.5} letterSpacing={1}>FOLD CHANGE SCALE</text>
                      {[...Array(50)].map((_,i)=>(
                        <rect key={i} x={lx+i*(lw/50)} y={ly} width={lw/50+0.5} height={lh} fill={foldColor((i/50)*5)}/>
                      ))}
                      {[0,1,2,3,4,5].map(v=>(
                        <text key={v} x={lx+(v/5)*lw} y={ly+lh+9} textAnchor="middle" fill={DIM} fontSize={7}>{v}.0</text>
                      ))}
                      <line x1={lx+(1/5)*lw} y1={ly-2} x2={lx+(1/5)*lw} y2={ly+lh+2} stroke="#aaa" strokeWidth={0.8}/>
                      <text x={lx+(1/5)*lw} y={ly-5} textAnchor="middle" fill="#aaa" fontSize={6.5}>1.0</text>
                    </g>
                  );
                })()}
              </svg>
            </div>
          </div>
        )}

        {/* ═══ DISTRIBUTIONS ═══ */}
        {tab==='dist' && (
          <div>
            {/* Gene selector */}
            <div style={{display:'flex',flexWrap:'wrap',gap:6,marginBottom:20}}>
              {GENES.map(g=>(
                <button key={g} onClick={()=>setSelG(g)}
                  style={{padding:'5px 11px',background:selG===g?ACCENT:'#0c1922',
                    color:selG===g?BG:DIM,border:`1px solid ${selG===g?ACCENT:'#182f44'}`,
                    borderRadius:3,fontSize:9,letterSpacing:0.5,cursor:'pointer',outline:'none',
                    fontFamily:"'Courier New',Courier,monospace"}}>
                  {g}
                </button>
              ))}
            </div>

            {(()=>{
              const cVals=CTRL.map(r=>r[selG]||0);
              const vVals=VDS.map(r=>r[selG]||0);
              const maxV=Math.max(...cVals,...vVals)*1.2;
              const PH=300,PW=600,PL=52,PB=36,PT=28;
              const plotH=PH-PB-PT;
              const toY=v=>PT+plotH-(v/maxV)*plotH;
              const cMean=cVals.reduce((a,c)=>a+c,0)/cVals.length;
              const vMean=vVals.reduce((a,c)=>a+c,0)/vVals.length;
              const cSD=Math.sqrt(cVals.reduce((a,c)=>a+(c-cMean)**2,0)/(cVals.length-1));
              const vSD=Math.sqrt(vVals.reduce((a,c)=>a+(c-vMean)**2,0)/(vVals.length-1));
              const ratio=vMean/cMean;
              const CX=PL+110, VX=PL+370;

              return (
                <div>
                  <svg width={PW} height={PH} onMouseLeave={()=>setTt(null)}>
                    {/* Title */}
                    <text x={PW/2} y={16} textAnchor="middle" fill={ACCENT} fontSize={12} letterSpacing={2} fontWeight="bold">{selG}</text>

                    {/* Y axis */}
                    <line x1={PL} y1={PT} x2={PL} y2={PH-PB} stroke="#1a3550" strokeWidth={1}/>
                    {[...Array(6)].map((_,i)=>{
                      const v=(maxV/5)*i, y=toY(v);
                      return (
                        <g key={i}>
                          <line x1={PL-4} y1={y} x2={PL} y2={y} stroke="#1a3550"/>
                          <text x={PL-6} y={y+3} textAnchor="end" fill={DIM} fontSize={8}>{v.toFixed(1)}</text>
                          <line x1={PL} y1={y} x2={PW-20} y2={y} stroke="#0c2030" strokeWidth={0.5}/>
                        </g>
                      );
                    })}
                    <line x1={PL} y1={toY(1)} x2={PW-20} y2={toY(1)} stroke="#1e4565" strokeWidth={1} strokeDasharray="5,3"/>
                    <text x={PW-18} y={toY(1)+3} fill="#1e4565" fontSize={7.5} textAnchor="middle">1.0</text>

                    {/* Y axis label */}
                    <text x={12} y={PT+plotH/2} textAnchor="middle" fill={DIM} fontSize={8.5} letterSpacing={1}
                      transform={`rotate(-90,12,${PT+plotH/2})`}>FOLD CHANGE</text>

                    {/* Control dots */}
                    <text x={CX} y={PH-10} textAnchor="middle" fill={CBLUE} fontSize={9} letterSpacing={1.5}>CONTROLS</text>
                    {/* SD bar */}
                    <line x1={CX} y1={toY(cMean+cSD)} x2={CX} y2={toY(cMean-cSD)} stroke={CBLUE} strokeWidth={1} opacity={0.35}/>
                    <line x1={CX-14} y1={toY(cMean+cSD)} x2={CX+14} y2={toY(cMean+cSD)} stroke={CBLUE} strokeWidth={0.8} opacity={0.35}/>
                    <line x1={CX-14} y1={toY(cMean-cSD)} x2={CX+14} y2={toY(cMean-cSD)} stroke={CBLUE} strokeWidth={0.8} opacity={0.35}/>
                    {/* Mean line */}
                    <line x1={CX-36} y1={toY(cMean)} x2={CX+36} y2={toY(cMean)} stroke={CBLUE} strokeWidth={2.5}/>
                    <text x={CX+44} y={toY(cMean)+3} fill={CBLUE} fontSize={9}>{cMean.toFixed(3)}</text>
                    {cVals.map((v,i)=>(
                      <g key={CTRL[i].id} style={{cursor:'crosshair'}}
                        onMouseEnter={()=>setTt({sample:CTRL[i].id,gene:selG,val:v,type:'CTRL',out:CTRL[i].out})}
                        onMouseLeave={()=>setTt(null)}>
                        <circle cx={CX+JITTER[i]} cy={toY(v)} r={5.5} fill={CTRL[i].out?'#ffaa44':CBLUE} opacity={0.85}/>
                        {CTRL[i].out&&<circle cx={CX+JITTER[i]} cy={toY(v)} r={8} fill="none" stroke="#ffaa44" strokeWidth={1}/>}
                      </g>
                    ))}

                    {/* VDS dots */}
                    <text x={VX} y={PH-10} textAnchor="middle" fill={VCORAL} fontSize={9} letterSpacing={1.5}>VDS</text>
                    <line x1={VX} y1={toY(vMean+vSD)} x2={VX} y2={toY(vMean-vSD)} stroke={VCORAL} strokeWidth={1} opacity={0.35}/>
                    <line x1={VX-14} y1={toY(vMean+vSD)} x2={VX+14} y2={toY(vMean+vSD)} stroke={VCORAL} strokeWidth={0.8} opacity={0.35}/>
                    <line x1={VX-14} y1={toY(vMean-vSD)} x2={VX+14} y2={toY(vMean-vSD)} stroke={VCORAL} strokeWidth={0.8} opacity={0.35}/>
                    <line x1={VX-36} y1={toY(vMean)} x2={VX+36} y2={toY(vMean)} stroke={VCORAL} strokeWidth={2.5}/>
                    <text x={VX+44} y={toY(vMean)+3} fill={VCORAL} fontSize={9}>{vMean.toFixed(3)}</text>
                    {vVals.map((v,i)=>(
                      <g key={VDS[i].id} style={{cursor:'crosshair'}}
                        onMouseEnter={()=>setTt({sample:VDS[i].id,gene:selG,val:v,type:'VDS'})}
                        onMouseLeave={()=>setTt(null)}>
                        <circle cx={VX+JITTER[i]} cy={toY(v)} r={5.5} fill={VCORAL} opacity={0.85}/>
                      </g>
                    ))}

                    {/* Connector dashed line */}
                    <line x1={CX+40} y1={toY(cMean)} x2={VX-40} y2={toY(vMean)} stroke="#1e4060" strokeWidth={1} strokeDasharray="4,4"/>
                  </svg>

                  {/* Stats row */}
                  <div style={{display:'flex',gap:10,marginTop:10,flexWrap:'wrap'}}>
                    {[
                      {l:'Ctrl Mean',v:cMean.toFixed(4),c:CBLUE},
                      {l:'Ctrl SD',v:'\u00b1'+cSD.toFixed(4),c:CBLUE},
                      {l:'VDS Mean',v:vMean.toFixed(4),c:VCORAL},
                      {l:'VDS SD',v:'\u00b1'+vSD.toFixed(4),c:VCORAL},
                      {l:'VDS / Ctrl',v:ratio.toFixed(3)+'x',c:ratio>1.25?'#ff8844':ratio<0.8?'#5599ff':ACCENT},
                    ].map(s=>(
                      <div key={s.l} style={{background:'#0c1922',border:'1px solid #182f44',borderRadius:4,padding:'8px 14px',minWidth:100}}>
                        <div style={{color:DIM,fontSize:8.5,letterSpacing:1,marginBottom:3}}>{s.l}</div>
                        <div style={{color:s.c,fontSize:13,fontWeight:'bold'}}>{s.v}</div>
                      </div>
                    ))}
                  </div>

                  {/* All-gene summary table */}
                  <div style={{marginTop:24}}>
                    <div style={{fontSize:9,color:DIM,letterSpacing:2,marginBottom:10}}>ALL GENES — MEAN COMPARISON</div>
                    <div style={{overflowX:'auto'}}>
                      <table style={{borderCollapse:'collapse',fontSize:9.5,width:'100%',maxWidth:720}}>
                        <thead>
                          <tr>
                            {['GENE','CTRL MEAN','CTRL SD','VDS MEAN','VDS SD','RATIO','DIRECTION'].map(h=>(
                              <th key={h} style={{padding:'6px 12px',textAlign:'left',color:DIM,fontWeight:'normal',
                                letterSpacing:1,borderBottom:'1px solid #0e2535',fontSize:8.5}}>{h}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {GENES.map((g,i)=>{
                            const cM=gmean(CTRL,g),vM=gmean(VDS,g);
                            const cS=gsd(CTRL,g),vS=gsd(VDS,g);
                            const r=vM/cM;
                            const up=r>1.25,dn=r<0.80;
                            const bg=g===selG?'#0c2035':'transparent';
                            return (
                              <tr key={g} style={{background:bg,cursor:'pointer'}} onClick={()=>setSelG(g)}>
                                <td style={{padding:'5px 12px',color:g.includes('\u2605')?ACCENT:'#7898b8',fontWeight:'bold'}}>{g}</td>
                                <td style={{padding:'5px 12px',color:CBLUE}}>{cM.toFixed(4)}</td>
                                <td style={{padding:'5px 12px',color:'#304860'}}>±{cS.toFixed(3)}</td>
                                <td style={{padding:'5px 12px',color:VCORAL}}>{vM.toFixed(4)}</td>
                                <td style={{padding:'5px 12px',color:'#603040'}}>±{vS.toFixed(3)}</td>
                                <td style={{padding:'5px 12px',color:up?'#ff8844':dn?'#5599ff':DIM,fontWeight:'bold'}}>{r.toFixed(3)}x</td>
                                <td style={{padding:'5px 12px',color:up?'#ff8844':dn?'#5599ff':DIM,fontSize:8.5}}>
                                  {up?'\u2191 HIGHER IN VDS':dn?'\u2193 LOWER IN VDS':'\u2014'}
                                </td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              );
            })()}
          </div>
        )}

        {/* ═══ QC FLAGS ═══ */}
        {tab==='qc' && (
          <div style={{maxWidth:660}}>
            <div style={{fontSize:9,color:DIM,letterSpacing:2,marginBottom:16}}>DATA QUALITY REVIEW · 3 FLAGS IDENTIFIED</div>
            {[
              {
                id:'QC-01',lv:'WARN',col:'#e0b040',
                title:'BCAS1 Standard Curve — Inversion Detected',
                body:'The 10% dilution (CT 27.72) is lower than the 100% (CT 28.99). More dilute template must yield higher CT. This indicates a pipetting or tube swap error on the BCAS1 plate. Original curve R²=0.7675. The corrected fit (BCAS1★, R²=0.972, slope=−0.303) is used in all calculations. Uncorrected BCAS1 values are suppressed.',
                fields:[['First curve R\u00b2','0.7675 \u2717'],['Corrected R\u00b2','0.9720 \u2713'],['10% CT vs 100% CT','27.72 < 28.99 (inverted)'],['Action','BCAS1\u2605 used throughout']],
              },
              {
                id:'QC-02',lv:'WARN',col:'#e0b040',
                title:'MOBP Standard Curve — Inversion Detected',
                body:'Same inversion: 10% dilution reads CT 25.83 while 100% reads CT 30.13. This is a ~4.3 CT paradox. The MOBP★ corrected values are used in all calculations and visualizations. Raw MOBP values should not be interpreted.',
                fields:[['10% CT','25.83'],['100% CT','30.13 (should be lower)'],['Paradox delta','\u22124.30 CT'],['Action','MOBP\u2605 correction applied']],
              },
              {
                id:'QC-03',lv:'FLAG',col:'#ff8033',
                title:'Control C6 — Probable RNA Input / Quality Outlier',
                body:'C6 shows GAPDH CT of 17.64 vs group median ~15.3, indicating ~3-fold lower RNA input or degraded RNA. This artificially inflates GAPDH-normalized fold changes for C6 across multiple targets. Downstream statistics should be run both including and excluding C6 to assess its influence on group differences.',
                fields:[['C6 GAPDH CT','17.64 (group median: ~15.3)'],['MBP fold change (C6)','3.09\u00d7 (group mean: ~0.77)'],['ERNM fold change (C6)','6.24\u00d7 (group mean: ~2.3)'],['Recommendation','Include/exclude sensitivity test']],
              },
            ].map(q=>(
              <div key={q.id} style={{background:'#0c1922',border:`1px solid ${q.col}44`,borderLeft:`3px solid ${q.col}`,
                borderRadius:4,padding:'16px 20px',marginBottom:14}}>
                <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:10}}>
                  <span style={{background:`${q.col}20`,color:q.col,padding:'2px 8px',borderRadius:2,fontSize:8.5,letterSpacing:1}}>
                    {q.lv} {q.id}
                  </span>
                  <span style={{color:'#98c0d8',fontSize:11,fontWeight:'bold'}}>{q.title}</span>
                </div>
                <p style={{color:'#506070',fontSize:10,lineHeight:1.75,margin:'0 0 12px'}}>{q.body}</p>
                <div style={{display:'flex',flexWrap:'wrap',gap:14}}>
                  {q.fields.map(([k,v])=>(
                    <div key={k} style={{fontSize:9}}>
                      <span style={{color:'#304860'}}>{k}: </span>
                      <span style={{color:'#80a8c0'}}>{v}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* TOOLTIP */}
      {tt && (
        <div style={{position:'fixed',left:mx+14,top:my-58,background:'#08161f',
          border:`1px solid ${tt.type==='VDS'?VCORAL:CBLUE}`,
          padding:'8px 13px',borderRadius:4,pointerEvents:'none',
          fontSize:11,zIndex:1000,boxShadow:'0 6px 24px rgba(0,0,0,0.7)'}}>
          <div style={{color:ACCENT,letterSpacing:1.5,fontSize:9.5}}>{tt.gene}</div>
          <div style={{marginTop:4,color:'#c0d8e8'}}>
            {tt.sample}&nbsp;&nbsp;<span style={{color:'#fff',fontWeight:'bold'}}>{tt.val.toFixed(4)}</span>
          </div>
          <div style={{color:tt.type==='VDS'?VCORAL:CBLUE,fontSize:8.5,letterSpacing:1,marginTop:2}}>
            {tt.type}{tt.out?' ⚠ OUTLIER':''}
          </div>
        </div>
      )}
    </div>
  );
}
