import React from 'react'
export default function SeverityBadge({ value = 'INFO', variant = 'pill' }) { return <span className={`severity severity-${value.toLowerCase()} ${variant === 'large' ? 'severity-large' : ''}`}><i />{value}</span> }
