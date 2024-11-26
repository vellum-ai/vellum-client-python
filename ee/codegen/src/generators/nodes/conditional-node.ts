import { python } from "@fern-api/python-ast";
import { Reference } from "@fern-api/python-ast/Reference";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { VellumValue } from "vellum-ai/api/types";

import { ConditionalNodeContext } from "src/context/node-context/conditional-node";
import { ConditionalNodePort } from "src/generators/conditional-node-port";
import { BaseSingleFileNode } from "src/generators/nodes/bases/single-file-base";
import {
  ConditionalNode as ConditionalNodeType,
  ConditionalNodeData,
  ConditionalRuleData,
} from "src/types/vellum";

export class ConditionalNode extends BaseSingleFileNode<
  ConditionalNodeType,
  ConditionalNodeContext
> {
  baseNodeClassName = "ConditionalNode";
  baseNodeDisplayClassName = "BaseConditionalNodeDisplay";

  protected getNodeClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    const inputVarIdsByRuleId = new Map<string, string>();
    const constantValuesByRuleIds = new Map<string, VellumValue>();
    this.constructMapsByRuleIds(inputVarIdsByRuleId, constantValuesByRuleIds);

    const baseNodeClassRef = this.getNodeBaseClass();

    const ref = python.reference({
      name: baseNodeClassRef.name,
      modulePath: baseNodeClassRef.modulePath,
      alias: baseNodeClassRef.alias,
      attribute: ["Ports"],
    });

    this.getNodeBaseClass().inheritReferences(ref);

    const portsClass = python.class_({
      name: "Ports",
      extends_: [ref],
    });
    Array.from(this.workflowContext.portContextById.entries()).forEach(
      ([portId, context], idx) => {
        const conditionData = this.nodeData.data.conditions.find(
          (condition) => condition.sourceHandleId === portId
        );

        if (!conditionData) {
          return;
        }

        const portName = `branch_${idx + 1}`;

        portsClass.addField(
          python.field({
            name: portName,
            initializer: new ConditionalNodePort({
              portContext: context,
              inputVarIdsByRuleId: inputVarIdsByRuleId,
              constantValuesByRuleIds: constantValuesByRuleIds,
              conditionData: conditionData,
            }),
          })
        );
      }
    );

    statements.push(portsClass);
    return statements;
  }

  protected getNodeDisplayClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    statements.push(
      python.field({
        name: "label",
        initializer: python.TypeInstantiation.str(this.nodeData.data.label),
      }),
      python.field({
        name: "node_id",
        initializer: python.TypeInstantiation.uuid(this.nodeData.id),
      }),
      python.field({
        name: "target_handle_id",
        initializer: python.TypeInstantiation.uuid(
          this.nodeData.data.targetHandleId
        ),
      })
    );

    statements.push(
      python.field({
        name: "source_handle_ids",
        initializer: python.TypeInstantiation.dict(
          this.nodeData.data.conditions.map((condition, idx) => ({
            key: python.TypeInstantiation.int(idx),
            value: python.TypeInstantiation.uuid(condition.sourceHandleId),
          }))
        ),
      })
    );

    const ruleIdMapRef = python.reference({
      name: "RuleIdMap",
      modulePath: [
        ...this.workflowContext.sdkModulePathNames.NODE_DISPLAY_MODULE_PATH,
        "vellum",
        "conditional_node",
      ],
    });

    this.getNodeDisplayBaseClass().inheritReferences(ruleIdMapRef);

    statements.push(
      python.field({
        name: "rule_ids",
        initializer: python.TypeInstantiation.list(
          this.createRuleIdMapList(this.nodeData.data, ruleIdMapRef)
        ),
      })
    );

    const conditionIdRef = python.reference({
      name: "ConditionId",
      modulePath: [
        ...this.workflowContext.sdkModulePathNames.NODE_DISPLAY_MODULE_PATH,
        "vellum",
        "conditional_node",
      ],
    });

    this.getNodeDisplayBaseClass().inheritReferences(conditionIdRef);

    statements.push(
      python.field({
        name: "condition_ids",
        initializer: python.TypeInstantiation.list(
          this.createConditionIdList(this.nodeData.data, conditionIdRef)
        ),
      })
    );

    return statements;
  }

  private createConditionIdList(
    nodeData: ConditionalNodeData,
    conditionIdRef: Reference
  ): AstNode[] {
    const conditionIdsList: AstNode[] = [];
    nodeData.conditions.forEach((condition) => {
      if (condition.data) {
        conditionIdsList.push(
          python.instantiateClass({
            classReference: conditionIdRef,
            arguments_: [
              python.methodArgument({
                name: "id",
                value: python.TypeInstantiation.uuid(condition.id),
              }),
              python.methodArgument({
                name: "rule_group_id",
                value: python.TypeInstantiation.uuid(condition.data.id),
              }),
            ],
          })
        );
      }
    });
    return conditionIdsList;
  }

  private createRuleIdMapList(
    nodeData: ConditionalNodeData,
    ruleIdMapRef: Reference
  ): AstNode[] {
    const ruleIdsList: AstNode[] = [];
    nodeData.conditions.forEach((condition) => {
      if (condition.data) {
        const ruleIdMap = this.createRuleIdMap(condition.data, ruleIdMapRef);
        if (ruleIdMap) {
          ruleIdsList.push(ruleIdMap);
        }
      }
    });

    return ruleIdsList;
  }

  private createRuleIdMap(
    ruleData: ConditionalRuleData,
    ruleIdMapRef: Reference
  ): AstNode | null {
    if (!ruleData) {
      return null;
    }

    let lhs = null;
    let rhs = null;

    // Check first rule in the arr (lhs)
    if (ruleData.rules && ruleData.rules[0]) {
      lhs = this.createRuleIdMap(ruleData.rules[0], ruleIdMapRef);
    }

    // Check second rule in the arr (rhs)
    if (ruleData.rules && ruleData.rules[1]) {
      rhs = this.createRuleIdMap(ruleData.rules[1], ruleIdMapRef);
    }

    return python.instantiateClass({
      classReference: ruleIdMapRef,
      arguments_: [
        python.methodArgument({
          name: "id",
          value: python.TypeInstantiation.uuid(ruleData.id),
        }),
        python.methodArgument({
          name: "lhs",
          value: lhs ? lhs : python.TypeInstantiation.none(),
        }),
        python.methodArgument({
          name: "rhs",
          value: rhs ? rhs : python.TypeInstantiation.none(),
        }),
      ],
    });
  }

  private constructMapsByRuleIds(
    inputVarIdsByRuleId: Map<string, string>,
    constantValuesByRuleIds: Map<string, unknown>
  ) {
    this.nodeData.inputs.forEach((input) => {
      const fieldIdx = input.key.indexOf(".field");
      const valueIdx = input.key.indexOf(".value");
      if (fieldIdx !== -1) {
        const ruleId = input.key.slice(0, fieldIdx);
        input.value.rules.forEach((rule) => {
          if (rule.type === "INPUT_VARIABLE") {
            inputVarIdsByRuleId.set(ruleId, rule.data.inputVariableId);
          }
        });
      } else if (valueIdx !== -1) {
        const ruleId = input.key.slice(0, valueIdx);
        input.value.rules.forEach((rule) => {
          let value: string | unknown;
          if (rule.type === "CONSTANT_VALUE") {
            value = rule.data;
          }
          constantValuesByRuleIds.set(ruleId, value);
        });
      }
    });
  }

  protected getErrorOutputId(): undefined {
    return undefined;
  }
}
