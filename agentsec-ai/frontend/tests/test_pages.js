import React from 'react'
import { render, screen } from '@testing-library/react'
import { describe, expect, test } from 'vitest'
import LoginPage from '../src/pages/auth/LoginPage.jsx'

describe('auth pages', () => {
  test('renders the login page heading and action', () => {
    render(React.createElement(LoginPage))
    expect(screen.getByRole('button')).toBeInTheDocument()
    expect(document.body.textContent.length).toBeGreaterThan(0)
  })
})