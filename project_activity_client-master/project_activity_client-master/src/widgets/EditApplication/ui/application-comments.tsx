import type { FC, FormEvent, ChangeEvent } from 'react';
import { useState, useEffect } from 'react';

import { useDispatch, useSelector } from '../../../store/store';

import { Form } from '../../../shared/components/Form/ui/form';
import {
	FormField,
	FormTextarea,
} from '../../../shared/components/Form/components';
import { Button } from '../../../shared/components/Button/ui/button';
import { Text } from '../../../shared/components/Typography';

import { convertDate } from '../../../shared/lib/date';
import { createCommentToFieldAction } from '../../../store/coordination/actions';

import styles from '../styles/application-comments.module.scss';

export const ApplicationComments: FC = () => {
	const dispatch = useDispatch();

	const [commentText, setCommentText] = useState<string>('');

	const { applicationDetail, currentField, isLoadingComment } = useSelector(
		(state) => state.coordination
	);

	const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
		setCommentText(e.target.value);
	};

	const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		if (!commentText.trim() || !applicationDetail || !currentField) return;

		try {
			await dispatch(
				createCommentToFieldAction({
					applicationId: applicationDetail.id,
					field: currentField.code,
					text: commentText,
				})
			).unwrap();
			setCommentText('');
		} catch (err) {
			console.error('Ошибка при создании комментария:', err);
		}
	};

	useEffect(() => {
		setCommentText('');
	}, [currentField]);

	if (!applicationDetail) {
		return;
	}

	const comments = currentField
		? applicationDetail.comments.filter(
				(elem) => elem.field === currentField.code
		  )
		: applicationDetail.comments;

	const isBlockSubmit = !commentText.trim() || isLoadingComment;

	return (
		<div className={styles.comments}>
			<div className={styles.header}>
				<p className={styles.header__subtitle}>
					{currentField ? 'Комментарии к полю' : 'Комментарии к заявке'}
				</p>
				<h3 className={styles.header__title}>
					{currentField ? currentField.name : applicationDetail.title}
				</h3>
			</div>
			{comments.length > 0 ? (
				<ul className={styles.list}>
					{comments.map((comment) => (
						<li key={comment.id} className={styles.comment}>
							<div className={styles.comment__header}>
								<span className={styles.comment__author}>
									{comment.author?.short_name || 'Неизвестный пользователь'}
								</span>
								<span className={styles.comment__role}>
									{comment.author?.role_name || ''}
								</span>
							</div>
							<p className={styles.comment__text}>{comment.text}</p>
							<span className={styles.comment__date}>
								{convertDate(comment.created_at)}
							</span>
						</li>
					))}
				</ul>
			) : (
				<Text text='Комментариев пока нет.' color='grey' withMarginTop />
			)}
			{currentField && (
				<div className={styles.form}>
					<Form
						name='form-add-comment-app'
						onSubmit={handleSubmit}
						formWidth='full'>
						<FormField title='Добавить комментарий'>
							<FormTextarea
								name='add-comment'
								value={commentText}
								onChange={handleChange}
								placeholder='Напишите комментарий...'
							/>
						</FormField>
						<Button
							style={{ margin: '0 0 0 auto' }}
							text='Отправить'
							type='submit'
							isBlock={isBlockSubmit}
							withIcon={{
								type: 'send',
								color: isBlockSubmit ? 'grey' : 'black',
							}}
						/>
					</Form>
				</div>
			)}
		</div>
	);
};
