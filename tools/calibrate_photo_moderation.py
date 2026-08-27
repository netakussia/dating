"""Run the photo-safety cascade over a labelled or unlabelled photo directory.

Usage: python -m tools.calibrate_photo_moderation path/to/photos
The report is deliberately aggregate-only: it prints no image data or face data.
"""

from __future__ import annotations

import argparse
import asyncio
from collections import Counter
from pathlib import Path

from config import get_settings
from services.photo_moderation_service import moderation_zone, normalize_image
from services.photo_safety_providers import (
    PhotoAssessment,
    PhotoSafetyProviderError,
    get_photo_safety_provider,
)

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}


async def calibrate(directory: Path) -> int:
    settings = get_settings()
    provider = get_photo_safety_provider(settings)
    totals: Counter[str] = Counter()
    # Telegram-exported files may be named ``photo.jpg (1)``; accept those too
    # and rely on the normalizer for the final format validation.
    candidates = [directory] if directory.is_file() else directory.rglob("*")
    files = [
        path
        for path in candidates
        if path.is_file()
        and (path.suffix.lower() in SUPPORTED or any(ext in path.name.lower() for ext in SUPPORTED))
    ]
    print(f"Calibrating {len(files)} photos with {provider.name}…", flush=True)
    for path in files:
        try:
            assessment = await provider.assess(normalize_image(path.read_bytes(), settings))
            zone = moderation_zone(assessment, nsfw_red_threshold=settings.nsfw_threshold)
            totals[zone] += 1
            print(
                f"{zone} {path.name}: face={assessment.face_score:.3f}; "
                f"human={assessment.human_score:.3f}; nsfw={assessment.nsfw_score:.3f}; "
                f"faces={assessment.face_count}"
            )
        except PhotoSafetyProviderError as error:
            # This is the same fail-soft policy as the bot: unavailable ML is a
            # yellow outcome, while the error remains visible in the report.
            fallback = PhotoAssessment(0.0, True, "ml_provider_fallback", 0.60, 1, 0.60, str(error))
            totals[moderation_zone(fallback)] += 1
            print(f"YELLOW {path.name}: {type(error).__name__}: {error}")
        except Exception as error:
            # Custom/development providers may use a different exception type;
            # calibration should still report the same fail-soft Yellow signal.
            fallback = PhotoAssessment(0.0, True, "ml_provider_fallback", 0.60, 1, 0.60, str(error))
            totals[moderation_zone(fallback, nsfw_red_threshold=settings.nsfw_threshold)] += 1
            print(f"YELLOW {path.name}: {type(error).__name__}: {error}")
        except (OSError, ValueError) as error:
            totals["ERROR"] += 1
            print(f"ERROR {path.name}: {type(error).__name__}")
    total = len(files)
    print(f"Photos: {total}")
    for zone in ("GREEN", "YELLOW", "RED", "ERROR"):
        count = totals[zone]
        percent = (count / total * 100) if total else 0
        print(f"{zone}: {count} ({percent:.1f}%)")
    return 0 if total else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Folder containing JPEG, PNG or WebP test photos")
    args = parser.parse_args()
    if not args.directory.is_file() and not args.directory.is_dir():
        parser.error(f"Not a file or directory: {args.directory}")
    return asyncio.run(calibrate(args.directory))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
