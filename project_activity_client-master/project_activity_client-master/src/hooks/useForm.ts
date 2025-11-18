import { useState, ChangeEvent, useCallback } from 'react';

interface ValidationRule {
	validate: (value: string) => boolean;
	errorMessage: string;
}

type ValidationSchema<T> = {
	[K in keyof T]?: ValidationRule[];
};

export function useForm<T>(
	initialValues: T,
	validationSchema: ValidationSchema<T>
) {
	const [values, setValues] = useState<T>(initialValues);
	const [errors, setErrors] = useState<{ [K in keyof T]?: string }>({});

	const validateField = useCallback(
		(name: keyof T, value: string) => {
			const fieldRules = validationSchema[name];
			if (!fieldRules) return;

			for (const rule of fieldRules) {
				if (!rule.validate(value)) {
					setErrors((prevErrors) => ({
						...prevErrors,
						[name]: rule.errorMessage,
					}));
					return;
				}
			}
			setErrors((prevErrors) => ({
				...prevErrors,
				[name]: '',
			}));
		},
		[validationSchema]
	);

	const handleChange = (
		event: ChangeEvent<HTMLInputElement> | ChangeEvent<HTMLTextAreaElement>
	) => {
		const { name, value } = event.target;
		setValues((prevValues) => ({
			...prevValues,
			[name]: value,
		}));

		validateField(name as keyof T, value);
	};

	const handleSelectChange = <K extends keyof T>(name: K, value: T[K]) => {
		setValues((prev) => ({ ...prev, [name]: value }));
	};

	const handleCheckboxToggle = <K extends keyof T>(name: K) => {
		setValues((prevValues) => ({
			...prevValues,
			[name]: !prevValues[name],
		}));
	};

	return {
		values,
		handleChange,
		handleSelectChange,
		handleCheckboxToggle,
		setValues,
		errors,
	};
}
