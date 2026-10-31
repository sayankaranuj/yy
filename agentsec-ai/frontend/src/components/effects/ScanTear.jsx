import React from 'react'
export default function ScanTear({ children, trigger = false }) { return <div className={trigger ? 'glitch-tear-once' : ''}>{children}</div> }
