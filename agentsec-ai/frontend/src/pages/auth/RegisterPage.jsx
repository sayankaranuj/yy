import React from 'react'
import MatrixRain from '../../components/effects/MatrixRain'
import Input from '../../components/ui/Input'
import Button from '../../components/ui/Button'
export default function RegisterPage() { return <main className="auth-page"><section className="auth-signal"><MatrixRain /><span className="eyebrow red">NEW OPERATOR</span><h1>MAP THE<br /><em>UNKNOWN.</em></h1><p>One account. Full visibility.</p></section><section className="auth-form"><span className="eyebrow">CREATE ACCOUNT</span><h2>REGISTER</h2><Input label="EMAIL" type="email" placeholder="operator@company.com" /><Input label="PASSWORD" type="password" placeholder="Create a strong password" /><Button>CREATE ACCOUNT</Button><p className="muted">Already registered? SIGN IN</p></section></main>}
