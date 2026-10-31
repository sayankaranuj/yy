import React from 'react'
export default function ScanModeBadge({ mode = 'CLASSIC' }) { return <span className={`mode mode-${mode.toLowerCase()}`}>{mode}</span> }
