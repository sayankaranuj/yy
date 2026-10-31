import React from 'react'
import ProgressBar from '../../components/ui/ProgressBar'
export default function LiveProgressDashboard({ target = 'northstar.io', progress = 0 }) { return <section className="scan-focus"><span className="eyebrow red">LIVE OPERATION</span><h3>{target}</h3><ProgressBar value={progress} /></section> }
