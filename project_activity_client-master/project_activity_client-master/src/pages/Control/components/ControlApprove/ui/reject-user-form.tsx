import type { FC, FormEvent, ChangeEvent } from 'react';

import { useState } from 'react';
import { useDispatch, useSelector } from '../../../../../store/store';

import { Form } from '../../../../../shared/components/Form/ui/form';
import {
	FormField,
	FormTextarea,
	FormButtons,
} from '../../../../../shared/components/Form/components';
import { Button } from '../../../../../shared/components/Button/ui/button';
import { UserData } from './user-data';

import { rejectUserAction } from '../../../../../store/control-approve/actions';

import styles from '../styles/control-approve.module.scss';

export const RejectUserForm: FC = () => {
	const dispatch = useDispatch();
	const { currentApproveUser, isLoadingRequest } = useSelector(
		(state) => state.controlApprove
	);

	const [reason, setReason] = useState('');
	const [error, setError] = useState('');

	const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
		setReason(e.target.value);
		if (e.target.value.trim()) {
			setError('');
		}
	};

	const isBlockSubmit = !reason.trim();

	const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		if (isBlockSubmit) {
			setError('Укажите причину отказа');
			return;
		}

		if (currentApproveUser) {
			const payload = {
				userId: currentApproveUser.id,
				reason,
			};

			dispatch(rejectUserAction(payload));
		}
	};

	if (!currentApproveUser) {
		return <p>Пользователь не найден!</p>;
	}

	return (
		<div className={styles.form}>
			<UserData user={currentApproveUser} />

			<Form
				name='form-control-user-reject'
				onSubmit={handleSubmit}
				formWidth='large'>
				<FormField
					title='Укажите причину для отказа:'
					fieldError={{
						text: error,
						isShow: !!error,
					}}>
					<FormTextarea name='reason' value={reason} onChange={handleChange} />
				</FormField>

				<FormButtons>
					<Button
						type='submit'
						text='Отказать'
						isBlock={isBlockSubmit || isLoadingRequest}
					/>
				</FormButtons>
			</Form>
		</div>
	);
};
