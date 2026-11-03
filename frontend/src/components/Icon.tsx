import {
  Award, BadgeCheck, Box, Building2, Calendar, Camera, ChartColumn, CircleCheck, Clapperboard, Clock, Code,
  Crown, FileSignature, Film, Ghost, Gift, GraduationCap, Handshake, Hash, Heart, Hotel, Layers, Lightbulb,
  ListChecks, MapPin, Megaphone, Mic, Music, Palette, Plane, SatelliteDish, Server, Shirt, Sparkles,
  SquarePen, Star, Target, Tv, Users, Video, Wine, Workflow, type LucideIcon,
} from "lucide-react";

// Doit rester synchronisé avec ICONES dans backend/catalog/models.py.
const ICONES: Record<string, LucideIcon> = {
  sparkles: Sparkles, clapperboard: Clapperboard, camera: Camera, video: Video, film: Film, palette: Palette,
  hash: Hash, "graduation-cap": GraduationCap, music: Music, mic: Mic, crown: Crown,
  "satellite-dish": SatelliteDish, tv: Tv, wine: Wine, megaphone: Megaphone, award: Award, target: Target,
  handshake: Handshake, users: Users, "badge-check": BadgeCheck, code: Code, "chart-column": ChartColumn,
  server: Server, ghost: Ghost, box: Box, "list-checks": ListChecks, "square-pen": SquarePen, gift: Gift,
  "file-signature": FileSignature, hotel: Hotel, "map-pin": MapPin, calendar: Calendar,
  "building-2": Building2, layers: Layers, workflow: Workflow, "circle-check": CircleCheck, heart: Heart,
  star: Star, plane: Plane, shirt: Shirt, clock: Clock, lightbulb: Lightbulb,
};

export default function Icon({ name, size = 24, className }: { name?: string; size?: number; className?: string }) {
  const Composant = (name && ICONES[name]) || Sparkles;
  return <Composant size={size} className={className} aria-hidden="true" strokeWidth={1.9} />;
}
