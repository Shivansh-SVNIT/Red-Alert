"use client";

import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, AlertTriangle, CheckCircle2, Satellite } from 'lucide-react';

export default function Dashboard() {
  const [data, setData] = useState<any[]>([]);
  const [isAnomaly, setIsAnomaly] = useState(false);

  useEffect(() => {
    // Fetch new data every 0.5 seconds to simulate a live stream
    const interval = setInterval(async () => {
      try {
        const response = await fetch('http://localhost:8000/next-frame');
        const newFrame = await response.json();
        
        // Update the anomaly status
        setIsAnomaly(newFrame.isAnomaly);
        
        // Add new frame to chart and keep only the last 30 data points
        setData(prevData => {
          const updatedData = [...prevData, newFrame];
          if (updatedData.length > 30) {
            return updatedData.slice(updatedData.length - 30);
          }
          return updatedData;
        });
        
      } catch (error) {
        console.error("Failed to fetch telemetry data:", error);
      }
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-200 p-8 font-mono">
      {/* HEADER */}
      <header className="flex items-center justify-between border-b border-slate-800 pb-6 mb-8">
        <div className="flex items-center gap-3">
          <Satellite className={`w-8 h-8 ${isAnomaly ? 'text-red-500 animate-bounce' : 'text-blue-400'}`} />
          <h1 className="text-2xl font-bold tracking-wider text-slate-100">
            RED-ALERT <span className={isAnomaly ? 'text-red-500' : 'text-blue-500'}>TELEMETRY</span>
          </h1>
        </div>
        
        {/* STATUS BADGE */}
        <div className={`flex items-center gap-2 px-4 py-2 rounded-full border transition-all duration-300 ${
          isAnomaly 
          ? 'bg-red-950/80 border-red-500 text-red-500 shadow-[0_0_15px_rgba(239,68,68,0.5)]' 
          : 'bg-emerald-950/50 border-emerald-500 text-emerald-500'
        }`}>
          {isAnomaly ? <AlertTriangle className="w-5 h-5 animate-pulse" /> : <CheckCircle2 className="w-5 h-5" />}
          <span className="font-semibold">{isAnomaly ? 'CRITICAL ANOMALY DETECTED' : 'SYSTEM NORMAL'}</span>
        </div>
      </header>

      {/* CHART SECTION */}
      <section className={`bg-slate-900 border rounded-xl p-6 shadow-2xl transition-all duration-300 ${
        isAnomaly ? 'border-red-900 shadow-[0_0_30px_rgba(239,68,68,0.15)]' : 'border-slate-800'
      }`}>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Activity className={`w-5 h-5 ${isAnomaly ? 'text-red-400' : 'text-slate-400'}`} />
            Channel 41 Live Feed
          </h2>
        </div>
        
        <div className="h-[400px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" stroke="#475569" fontSize={12} />
              <YAxis domain={['auto', 'auto']} stroke="#475569" fontSize={12} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#020617', borderColor: '#1e293b', color: '#f8fafc' }}
                itemStyle={{ color: isAnomaly ? '#ef4444' : '#38bdf8' }}
              />
              <Line 
                type="monotone" 
                dataKey="ch41" 
                stroke={isAnomaly ? '#ef4444' : '#3b82f6'} 
                strokeWidth={3}
                dot={isAnomaly ? { fill: '#ef4444', strokeWidth: 2, r: 4 } : false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>
    </main>
  );
}