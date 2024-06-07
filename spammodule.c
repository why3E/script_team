#include "Python.h"
#include <stdlib.h>
#include <string.h>

// 비교 함수 정의
int compare_strings(const void* a, const void* b) {
    return strcmp(*(const char**)a, *(const char**)b);
}

// 리스트를 받아 정렬하는 함수
static PyObject*
spam_sort(PyObject* self, PyObject* args)
{
    PyObject* listObj;
    int descending;

    // 리스트 객체와 내림차순 여부를 파싱합니다.
    if (!PyArg_ParseTuple(args, "O!p", &PyList_Type, &listObj, &descending))
        return NULL;

    // 리스트의 길이를 가져옵니다.
    Py_ssize_t len = PyList_Size(listObj);
    if (len < 0)
        return NULL;

    // 리스트를 C 문자열 배열로 복사합니다.
    const char** strings = (const char**)malloc(len * sizeof(const char*));
    if (!strings)
        return PyErr_NoMemory();

    for (Py_ssize_t i = 0; i < len; i++) {
        PyObject* item = PyList_GetItem(listObj, i);
        if (!item) {
            free(strings);
            return NULL;
        }

        strings[i] = PyUnicode_AsUTF8(item);
        if (!strings[i]) {
            free(strings);
            return NULL;
        }
    }

    // qsort를 사용하여 정렬합니다.
    qsort(strings, len, sizeof(const char*), compare_strings);

    // 만약 내림차순이라면 리스트를 뒤집습니다.
    if (descending) {
        for (Py_ssize_t i = 0; i < len / 2; i++) {
            const char* temp = strings[i];
            strings[i] = strings[len - i - 1];
            strings[len - i - 1] = temp;
        }
    }

    // 정렬된 문자열을 Python 리스트로 변환합니다.
    PyObject* sortedList = PyList_New(len);
    if (!sortedList) {
        free(strings);
        return NULL;
    }

    for (Py_ssize_t i = 0; i < len; i++) {
        PyObject* item = PyUnicode_FromString(strings[i]);
        if (!item) {
            free(strings);
            Py_DECREF(sortedList);
            return NULL;
        }
        PyList_SET_ITEM(sortedList, i, item);
    }

    free(strings);

    return sortedList; // 정렬된 리스트를 반환합니다.
}

static PyMethodDef SpamMethods[] = {
    { "sort", spam_sort, METH_VARARGS, "Sort a list of strings. Pass True for descending order and False for ascending order." },
    { NULL, NULL, 0, NULL } // 배열의 끝을 나타냅니다.
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",               // 모듈 이름
    "It is test module.", // 모듈 설명을 적는 부분, 모듈의 __doc__에 저장됩니다.
    -1, SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}
