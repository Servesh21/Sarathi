/**
 * Sarathi Theme - Designed for low digital literacy, high accessibility
 * Focus: Clean, data-first fintech meets wellness tracker
 */

import { Platform } from 'react-native';

// Deep calming green - signifying growth and safety
const primaryGreen = '#047857';
const primaryGreenLight = '#10b981';

// Bright motivational yellow/orange for CTAs
const actionOrange = '#f59e0b';
const actionYellow = '#fbbf24';

export const Colors = {
  light: {
    // Primary brand colors
    primary: primaryGreen,
    primaryLight: primaryGreenLight,
    primaryDark: '#065f46',

    // Action colors - bright and motivational
    action: actionOrange,
    actionLight: actionYellow,

    // Status colors
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',

    // Neutral colors - clean and high contrast
    background: '#ffffff',
    backgroundSecondary: '#f9fafb',
    backgroundCard: '#f3f4f6',

    // Text colors - high contrast for readability
    text: '#111827',
    textSecondary: '#6b7280',
    textLight: '#9ca3af',
    textInverse: '#ffffff',

    // Border colors
    border: '#e5e7eb',
    borderLight: '#f3f4f6',

    // Legacy mappings for compatibility
    tint: primaryGreen,
    icon: '#6b7280',
    tabIconDefault: '#9ca3af',
    tabIconSelected: primaryGreen,
  },
  dark: {
    // Primary colors
    primary: primaryGreenLight,
    primaryLight: '#34d399',
    primaryDark: '#059669',

    // Action colors
    action: actionYellow,
    actionLight: '#fcd34d',

    // Status colors
    success: '#10b981',
    warning: '#fbbf24',
    danger: '#f87171',

    // Neutral colors
    background: '#111827',
    backgroundSecondary: '#1f2937',
    backgroundCard: '#374151',

    // Text colors
    text: '#f9fafb',
    textSecondary: '#d1d5db',
    textLight: '#9ca3af',
    textInverse: '#111827',

    // Border colors
    border: '#374151',
    borderLight: '#4b5563',

    // Legacy mappings
    tint: primaryGreenLight,
    icon: '#9ca3af',
    tabIconDefault: '#6b7280',
    tabIconSelected: primaryGreenLight,
  },
};

// Typography scale - large, friendly, legible (Inter/Nunito Sans style)
export const Typography = {
  hero: 48,     // Today's Net Profit
  xxl: 36,      // Major headings
  xl: 28,       // Section headings
  lg: 20,       // Card titles
  md: 16,       // Body text
  sm: 14,       // Secondary text
  xs: 12,       // Labels
};

// Spacing scale
export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

// Border radius
export const Radius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  full: 9999,
};

export const Fonts = Platform.select({
  ios: {
    /** iOS `UIFontDescriptorSystemDesignDefault` */
    sans: 'system-ui',
    /** iOS `UIFontDescriptorSystemDesignSerif` */
    serif: 'ui-serif',
    /** iOS `UIFontDescriptorSystemDesignRounded` */
    rounded: 'ui-rounded',
    /** iOS `UIFontDescriptorSystemDesignMonospaced` */
    mono: 'ui-monospace',
  },
  default: {
    sans: 'normal',
    serif: 'serif',
    rounded: 'normal',
    mono: 'monospace',
  },
  web: {
    sans: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    serif: "Georgia, 'Times New Roman', serif",
    rounded: "'SF Pro Rounded', 'Hiragino Maru Gothic ProN', Meiryo, 'MS PGothic', sans-serif",
    mono: "SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
  },
});
