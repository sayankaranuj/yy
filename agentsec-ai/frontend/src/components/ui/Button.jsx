import React from 'react'
export default function Button({ children, variant = 'primary', loading = false, ...props }) { return <button className={`btn ${variant}`} disabled={loading || props.disabled} {...props}>{loading ? '...' : children}</button> }
