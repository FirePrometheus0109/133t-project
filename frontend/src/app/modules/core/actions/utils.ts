/**
 * This function coerces a string into a string literal type.
 * Using tagged union types in TypeScript 2.0, this enables
 * powerful type checking of reducers.
 *
 * Since every action label passes through this function it
 * is a good place to ensure the action labels are unique.
 */

const typeCache: { [label: string]: boolean } = {};

export function createActionType<T>(label: T | ''): T {
  if (typeCache[<string>label]) {
    throw new Error(`Action type "${label}" is not unique"`);
  }

  typeCache[<string>label] = true;

  return <T>label;
}
