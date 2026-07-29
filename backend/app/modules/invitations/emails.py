"""Invitation email content. Professional and restrained — company + role context, why
they're receiving it, one clear CTA, expiry, and what's next. No internal terminology
(never "CandidateEvaluation"), no scoring/AI details, no internal IDs."""

from datetime import datetime

from app.platform.email import EmailMessage


def build_invitation_email(
    *,
    to: str,
    candidate_name: str,
    organization_name: str,
    role_title: str,
    link: str,
    expires_at: datetime,
) -> EmailMessage:
    expires = expires_at.date().isoformat()  # portable, unambiguous (YYYY-MM-DD)
    first_name = candidate_name.split()[0] if candidate_name.strip() else "there"
    subject = f"{organization_name}: your {role_title} work sample"

    text_body = (
        f"Hi {first_name},\n\n"
        f"{organization_name} has invited you to complete a short work sample for the "
        f"{role_title} role. It's a chance to show your skills through real work rather "
        f"than a résumé alone.\n\n"
        f"Get started: {link}\n\n"
        f"This link is personal to you and expires on {expires}.\n\n"
        f"What happens next: you'll review a few details and give your consent, then "
        f"complete the work sample at your own pace. Your submission is reviewed by the "
        f"hiring team — a person makes the decision.\n"
    )

    container_style = (
        "font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;"
        "max-width:480px;margin:0 auto;color:#0b1020;line-height:1.55"
    )
    button_style = (
        "background:#4f46e5;color:#fff;text-decoration:none;padding:12px 20px;"
        "border-radius:10px;font-weight:600;font-size:15px;display:inline-block"
    )
    muted = "font-size:13px;color:#556565"

    html_body = "".join(
        [
            f'<div style="{container_style}">',
            f'<p style="font-size:15px">Hi {first_name},</p>',
            '<p style="font-size:15px">',
            f"<strong>{organization_name}</strong> has invited you to complete a short work "
            f"sample for the <strong>{role_title}</strong> role — a chance to show your skills "
            "through real work rather than a résumé alone.",
            "</p>",
            f'<p style="margin:28px 0"><a href="{link}" style="{button_style}">'
            "Review &amp; continue</a></p>",
            f'<p style="{muted}">This link is personal to you and expires on {expires}.</p>',
            f'<p style="{muted}">What happens next: you\'ll review a few details and give your '
            "consent, then complete the work sample at your own pace. Your submission is "
            "reviewed by the hiring team — a person makes the decision.</p>",
            "</div>",
        ]
    )
    return EmailMessage(to=to, subject=subject, html_body=html_body, text_body=text_body)
