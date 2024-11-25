import { BaseNodeInputValuePointerRule } from "./base";

import * as codegen from "src/codegen";
import { VellumValue } from "src/generators";
import { ConstantValuePointer } from "src/types/vellum";

export class ConstantValuePointerRule extends BaseNodeInputValuePointerRule<ConstantValuePointer> {
  getAstNode(): VellumValue {
    const constantValuePointerRuleData = this.nodeInputValuePointerRule.data;

    return codegen.vellumValue({ vellumValue: constantValuePointerRuleData });
  }
}
