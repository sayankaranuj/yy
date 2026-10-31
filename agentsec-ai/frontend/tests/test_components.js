import React from 'react'
import { render, screen } from '@testing-library/react'
import { describe, expect, test } from 'vitest'
import Button from '../src/components/ui/Button.jsx'
import ProgressBar from '../src/components/ui/ProgressBar.jsx'
import SeverityBadge from '../src/components/ui/SeverityBadge.jsx'

describe('shared components', () => {
  test('renders severity text and class', () => {
    render(React.createElement(SeverityBadge, { value: 'CRITICAL' }))
    const badge = screen.getByText('CRITICAL')
    expect(badge).toHaveClass('severity-critical')
  })

  test('renders progress value as a width', () => {
    render(React.createElement(ProgressBar, { value: 60 }))
    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '60')
    expect(screen.getByRole('progressbar').firstElementChild).toHaveStyle({ width: '60%' })
  })

  test('disables a loading button', () => {
    render(React.createElement(Button, { loading: true }, 'Submit'))
    expect(screen.getByRole('button')).toBeDisabled()
    expect(screen.getByRole('button')).toHaveTextContent('...')
  })
})