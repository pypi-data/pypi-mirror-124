use crate::{
    compilation::{compile_validators, context::CompilationContext, JSONSchema},
    error::{error, no_error, ErrorIterator, ValidationError},
    keywords::CompilationResult,
    paths::{InstancePath, JSONPointer},
    validator::{format_validators, Validate, Validators},
};
use serde_json::{Map, Value};

pub(crate) struct ContainsValidator {
    validators: Validators,
    schema_path: JSONPointer,
}

impl ContainsValidator {
    #[inline]
    pub(crate) fn compile<'a>(
        schema: &'a Value,
        context: &CompilationContext,
    ) -> CompilationResult<'a> {
        let keyword_context = context.with_path("contains");
        Ok(Box::new(ContainsValidator {
            validators: compile_validators(schema, &keyword_context)?,
            schema_path: keyword_context.into_pointer(),
        }))
    }
}

impl Validate for ContainsValidator {
    fn is_valid(&self, schema: &JSONSchema, instance: &Value) -> bool {
        if let Value::Array(items) = instance {
            for item in items {
                if self
                    .validators
                    .iter()
                    .all(|validator| validator.is_valid(schema, item))
                {
                    return true;
                }
            }
            false
        } else {
            true
        }
    }

    fn validate<'a, 'b>(
        &self,
        schema: &'a JSONSchema,
        instance: &'b Value,
        instance_path: &InstancePath,
    ) -> ErrorIterator<'b> {
        if let Value::Array(items) = instance {
            for item in items {
                if self
                    .validators
                    .iter()
                    .all(|validator| validator.is_valid(schema, item))
                {
                    return no_error();
                }
            }
            error(ValidationError::contains(
                self.schema_path.clone(),
                instance_path.into(),
                instance,
            ))
        } else {
            no_error()
        }
    }
}

impl core::fmt::Display for ContainsValidator {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "contains: {}", format_validators(&self.validators))
    }
}

#[inline]
pub(crate) fn compile<'a>(
    _: &'a Map<String, Value>,
    schema: &'a Value,
    context: &CompilationContext,
) -> Option<CompilationResult<'a>> {
    Some(ContainsValidator::compile(schema, context))
}

#[cfg(test)]
mod tests {
    use crate::tests_util;
    use serde_json::json;

    #[test]
    fn schema_path() {
        tests_util::assert_schema_path(&json!({"contains": {"const": 2}}), &json!([]), "/contains")
    }
}
