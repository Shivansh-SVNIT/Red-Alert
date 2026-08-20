"use client";

import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Activity, AlertTriangle, CheckCircle2, Satellite, Zap, Thermometer, Compass, Radio, ShieldAlert } from 'lucide-react';

export default function Dashboard() {
  const [data, setData] = useState<any[]>([]);
  const [currentFrame, setCurrentFrame] = useState<any>({
    time: "--:--:--",
    ch41: 0.8000,
    temperature: 24.5,
    busVoltage: 28.2,
    gyroDrift: 0.012,
    riskScore: 0.0,
    isAnomaly: false
  });

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch('http://localhost:8000/next-frame');
        const newFrame = await response.json();
        
        setCurrentFrame(newFrame);
        
        setData(prevData => {
          const updatedData = [...prevData, newFrame];
          if (updatedData.length > 35) {
            return updatedData.slice(updatedData.length - 35);
          }
          return updatedData;
        });
        
      } catch (error) {
        console.error("Failed to fetch telemetry data:", error);
      }
    }, 500);

    return () => clearInterval(interval);
  }, []);

  const isAnomaly = currentFrame.isAnomaly;

  return (
    <main className="min-h-screen bg-slate-950 text-slate-200 p-6 lg:p-8 font-mono">
      {/* TOP HEADER */}
      <header className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-slate-800 pb-5 mb-6 gap-4">
        <div className="flex items-center gap-3">
          <Satellite className={`w-8 h-8 ${isAnomaly ? 'text-red-500 animate-bounce' : 'text-cyan-400'}`} />
          <div>
            <h1 className="text-xl sm:text-2xl font-bold tracking-wider text-slate-100 flex items-center gap-2">
              ISRO RED-ALERT <span className={isAnomaly ? 'text-red-500' : 'text-cyan-400'}>TELEMETRY TWIN</span>
            </h1>
            <p className="text-xs text-slate-500">Live Mission Subsystem Health & AI Anomaly Stream</p>
          </div>
        </div>
        
        {/* STATUS BADGE */}
        <div className={`flex items-center gap-2.5 px-4 py-2 rounded-full border transition-all duration-300 ${
          isAnomaly 
          ? 'bg-red-950/80 border-red-500 text-red-400 shadow-[0_0_20px_rgba(239,68,68,0.4)]' 
          : 'bg-emerald-950/50 border-emerald-500 text-emerald-400'
        }`}>
          {isAnomaly ? <AlertTriangle className="w-5 h-5 animate-pulse" /> : <CheckCircle2 className="w-5 h-5" />}
          <span className="text-xs sm:text-sm font-semibold tracking-wide">
            {isAnomaly ? 'CRITICAL SUBSYSTEM FAULT DETECTED' : 'ALL SUBSYSTEMS NOMINAL'}
          </span>
        </div>
      </header>

      {/* METRIC CARDS */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {/* Primary Bus Voltage */}
        <div className={`bg-slate-900 border rounded-xl p-4 transition-all ${isAnomaly ? 'border-red-500/50' : 'border-slate-800'}`}>
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold">EPS BUS VOLTAGE</span>
            <Zap className={`w-4 h-4 ${isAnomaly ? 'text-red-400' : 'text-amber-400'}`} />
          </div>
          <div className="text-xl sm:text-2xl font-bold text-slate-100">{currentFrame.busVoltage} V</div>
          <span className="text-[10px] text-slate-500">Nominal: 28.0V &plusmn; 0.5V</span>
        </div>

        {/* Core Temperature */}
        <div className={`bg-slate-900 border rounded-xl p-4 transition-all ${isAnomaly ? 'border-red-500/50' : 'border-slate-800'}`}>
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold">TCS CORE TEMP</span>
            <Thermometer className={`w-4 h-4 ${isAnomaly ? 'text-red-400' : 'text-blue-400'}`} />
          </div>
          <div className="text-xl sm:text-2xl font-bold text-slate-100">{currentFrame.temperature} &deg;C</div>
          <span className="text-[10px] text-slate-500">Safe Range: -10&deg;C to +45&deg;C</span>
        </div>

        {/* Gyro Drift */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold">AOCS GYRO DRIFT</span>
            <Compass className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-xl sm:text-2xl font-bold text-slate-100">{currentFrame.gyroDrift} &deg;/s</div>
          <span className="text-[10px] text-slate-500">Tolerance: &lt; 0.050 &deg;/s</span>
        </div>

        {/* Anomaly Risk Probability */}
        <div className={`bg-slate-900 border rounded-xl p-4 transition-all ${
          isAnomaly ? 'border-red-500 bg-red-950/20' : 'border-slate-800'
        }`}>
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold">AI RISK SCORE</span>
            <ShieldAlert className={`w-4 h-4 ${isAnomaly ? 'text-red-400' : 'text-emerald-400'}`} />
          </div>
          <div className={`text-xl sm:text-2xl font-bold ${isAnomaly ? 'text-red-400' : 'text-emerald-400'}`}>
            {currentFrame.riskScore}%
          </div>
          <span className="text-[10px] text-slate-500">Random Forest Ensemble</span>
        </div>
      </div>

      {/* CHART & SUBSYSTEM MATRIX GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* MAIN CHART */}
        <section className={`lg:col-span-2 bg-slate-900 border rounded-xl p-5 shadow-2xl transition-all ${
          isAnomaly ? 'border-red-900/80 shadow-[0_0_30px_rgba(239,68,68,0.1)]' : 'border-slate-800'
        }`}>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold flex items-center gap-2 text-slate-200">
              <Activity className={`w-4 h-4 ${isAnomaly ? 'text-red-400' : 'text-cyan-400'}`} />
              Channel 41 (EPS Primary Sensor Stream)
            </h2>
            <span className="text-xs text-slate-500 font-normal">Last Frame: {currentFrame.time}</span>
          </div>
          
          <div className="h-[340px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data} margin={{ top: 10, right: 10, bottom: 5, left: -20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="time" stroke="#475569" fontSize={11} />
                <YAxis domain={['auto', 'auto']} stroke="#475569" fontSize={11} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#020617', borderColor: '#334155', color: '#f8fafc', borderRadius: '8px' }}
                  itemStyle={{ color: isAnomaly ? '#ef4444' : '#38bdf8' }}
                />
                <ReferenceLine y={0.808} stroke="#ef4444" strokeDasharray="3 3" label={{ value: "Warning Threshold", fill: "#ef4444", fontSize: 10 }} />
                <Line 
                  type="monotone" 
                  dataKey="ch41" 
                  stroke={isAnomaly ? '#ef4444' : '#0ea5e9'} 
                  strokeWidth={2.5}
                  dot={isAnomaly ? { fill: '#ef4444', r: 3 } : false}
                  isAnimationActive={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

        {/* SUBSYSTEM STATUS PANEL */}
        <section className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-slate-200 mb-4 flex items-center gap-2">
              <Radio className="w-4 h-4 text-cyan-400" />
              Subsystem Health Matrix
            </h3>
            
            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                <span className="text-slate-300">Electrical Power (EPS)</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${isAnomaly ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                  {isAnomaly ? 'WARNING' : 'HEALTHY'}
                </span>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                <span className="text-slate-300">Thermal Control (TCS)</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${isAnomaly ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                  {isAnomaly ? 'ELEVATED' : 'HEALTHY'}
                </span>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                <span className="text-slate-300">Attitude Control (AOCS)</span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400">
                  HEALTHY
                </span>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
                <span className="text-slate-300">Comm & TT&C</span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400">
                  HEALTHY
                </span>
              </div>
            </div>
          </div>

          {/* PREDICTIVE ACTION BOX */}
          <div className={`mt-4 p-3 rounded-lg border text-xs ${
            isAnomaly 
            ? 'bg-red-950/30 border-red-500/40 text-red-300' 
            : 'bg-slate-950/50 border-slate-800 text-slate-400'
          }`}>
            <strong className="block mb-1 text-slate-200">
              {isAnomaly ? 'Recommended Action:' : 'System Status:'}
            </strong>
            {isAnomaly 
              ? 'Telemetry variance exceeds 3-sigma band. Initiate EPS secondary bus routing & reduce payload duty cycle.'
              : 'Telemetry parameters operating within nominal baseline bounds. Next orbit contact scheduled.'}
          </div>
        </section>
      </div>
    </main>
  );
}