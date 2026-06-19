export function mapValidationErrors(details) {
  const mapped = {};
  for (const item of details || []) {
    const field = item.loc?.[item.loc.length - 1];
    if (field) {
      mapped[field] = item.msg;
    }
  }
  return mapped;
}
