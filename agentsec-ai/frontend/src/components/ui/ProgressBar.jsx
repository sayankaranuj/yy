import React from 'react'
export default function ProgressBar({ value = 0 }) { return <div className="progress" role="progressbar" aria-valuenow={value} aria-valuemin="0" aria-valuemax="100"><span style={{ width: `${value}%` }} /></div> }
