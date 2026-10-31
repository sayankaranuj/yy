import React from 'react'
import MatrixRain from '../../components/effects/MatrixRain'
import Input from '../../components/ui/Input'
import Button from '../../components/ui/Button'
export default function LoginPage() { return <main className="auth-page"><section className="auth-signal"><MatrixRain /><span className="eyebrow red">FOUND FIRST</span><h1>SEE THE<br /><em>EXPOSURE.</em></h1><p>Autonomous attack surface intelligence for teams that cannot afford blind spots.</p></section><section className="auth-form"><span className="eyebrow">OPERATOR ACCESS</span><h2>CONTINUE</h2><Input label="EMAIL" type="email" placeholder="operator@company.com" /><Input label="PASSWORD" type="password" placeholder="••••••••" /><Button>CONTINUE</Button><p className="muted">No account? CREATE ACCOUNT</p></section></main>}
