import type { FC, FormEvent } from 'react';

import { PublicLayout } from '../../../shared/components/Layout/PublicLayout/ui/public-layout';
import { Section } from '../../../shared/components/Section/ui/section';
import { Form } from '../../../shared/components/Form/ui/form';
import { FormField } from '../../../shared/components/Form/components/FormField/form-field';
import { FormInput } from '../../../shared/components/Form/components/FormInput/form-input';
import { FormLinks } from '../../../shared/components/Form/components/FormLinks/form-links';

import { useForm } from '../../../hooks/useForm';
import { required, emailFormat } from '../../../shared/lib/validationRules';

import styles from '../styles/forgot-password.module.scss';

const links = [{ label: 'Вспомнили пароль?', text: 'Войти', url: '/' }];

interface IForgotPasswordForm {
	email: string;
}

const validationSchema = {
	email: [
		required('Введите электронную почту'),
		emailFormat('Неверный формат электронной почты'),
	],
};

export const ForgotPassword: FC = () => {
	const { values, handleChange, errors } = useForm<IForgotPasswordForm>(
		{ email: '' },
		validationSchema
	);

	const handleLogin = (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		if (!errors.email) {
			console.log('Форма отправлена', values);
		} else {
			console.log('Ошибки в форме');
		}
	};

	return (
		<PublicLayout>
			<main className={styles.container}>
				<Section>
					<Form
						name='form-forgot-password'
						onSubmit={handleLogin}
						title='Запрос на сброс пароля'
						titleAlign='center'>
						<FormField
							title='Электронная почта:'
							fieldError={{ text: errors.email || '', isShow: !!errors.email }}>
							<FormInput
								name='email'
								value={values.email}
								onChange={handleChange}
							/>
						</FormField>
					</Form>
				</Section>
				<FormLinks links={links} />
			</main>
		</PublicLayout>
	);
};
