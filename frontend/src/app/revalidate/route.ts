import { revalidateTag } from "next/cache";
import { NextResponse } from "next/server";

// Appelé par Django après chaque modification dans l'admin pour afficher
// immédiatement le nouveau contenu.
export async function POST(request: Request) {
  const secret = process.env.REVALIDATE_SECRET;
  if (!secret || request.headers.get("x-revalidate-secret") !== secret) {
    return NextResponse.json({ ok: false }, { status: 401 });
  }
  revalidateTag("cms", { expire: 0 });
  return NextResponse.json({ ok: true });
}
