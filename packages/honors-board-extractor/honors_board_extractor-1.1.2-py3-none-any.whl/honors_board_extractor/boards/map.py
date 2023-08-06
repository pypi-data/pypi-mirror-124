from pandas import DataFrame


def board_map(df: DataFrame, assignments: DataFrame) -> DataFrame:
    """
    Mutates and adds columns to the DataFrame.

    This function will set is_honors to false for every student
    that is high honors. It will add the initials column, the honors
    grade column, and the current subject column.

    Required columns are: is_honors, is_high_honors, school_grade,
    firstname, and lastname.

    Required columns for assignments are user_id and honor_status.honor_grade.
    """
    return (
        df
        .pipe(_add_initials)
        .pipe(_fix_honors_overlap)
        .pipe(_add_current_subject)
        .pipe(_add_honors_grade, assignments)
        .pipe(_format_start_date)
    )


_subject_grade_map = {
    '1': 'Grade 1',
    '2': 'Grade 2',
    '3': 'Grade 3',
    '4': 'Grade 4',
    '5': 'Grade 5',
    '6': 'Grade 6',
    '7': 'Grade 7',
    '8': 'Grade 8',
    '9': 'Algebra I',
    '10': 'Geometry',
    '11': 'Algebra II',
    '12': 'Pre-Calculus',
}

_grade_subject_map = {
    'Grade 1': 1,
    'Grade 2': 2,
    'Grade 3': 3,
    'Grade 4': 4,
    'Grade 5': 5,
    'Grade 6': 6,
    'Grade 7': 7,
    'Grade 8': 8,
    'Algebra I': 9,
    'Geometry': 10,
    'Algebra II': 11,
    'Pre-Calculus': 12,
    14: 14
}


def _add_initials(df: DataFrame) -> DataFrame:
    return df.assign(
        initials=df.firstname.str.capitalize() + ' ' + df.lastname.str.capitalize().str.get(0) + '.'
    )


def _fix_honors_overlap(df: DataFrame) -> DataFrame:
    ret = df.copy()
    ret.loc[ret.is_high_honor.isna(), 'is_high_honor'] = False
    ret.loc[ret.is_honor.isna(), 'is_honor'] = False
    ret.loc[ret.is_high_honor, 'is_honor'] = False
    ret.is_honor = ret.is_honor.astype('bool')
    ret.is_high_honor = ret.is_high_honor.astype('bool')
    return ret


def _add_current_subject(df: DataFrame) -> DataFrame:
    return df.assign(
        current_subject=df.current_grade.apply(lambda x: _subject_grade_map[x]),
        current_grade=lambda x: x['current_subject'].apply(lambda y: _grade_subject_map[y])
    )


def _add_honors_grade(df: DataFrame, assignments: DataFrame) -> DataFrame:
    """
    Default behavior is to set missing honor grades to 14. This way
    those students with missing honors grades won't be included in the
    almost honors category.
    """
    ret = df.copy()
    assign = assignments.loc[:, ['user_id', 'honor_status.honor_grade']].copy()
    ret = ret.merge(assign, on='user_id', how='left')
    ret.rename(columns={'honor_status.honor_grade': 'honor_grade'}, inplace=True)
    ret.loc[ret.honor_grade.isna(), 'honor_grade'] = 14
    ret = ret.assign(
        honor_grade=ret.honor_grade.apply(lambda x: _grade_subject_map[x])
    )
    return ret


def _format_start_date(df: DataFrame) -> DataFrame:
    return df.assign(
        start_ts=df.start_ts.str.slice(start=0, stop=10)
    )
