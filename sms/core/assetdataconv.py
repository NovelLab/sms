"""Data converter for assets data."""

# Official Libraries
import yaml
from typing import Any


# My Modules
from sms.objs.baseobject import SObject
from sms.objs.item import Item
from sms.objs.nametag import NameTag, NameTagType
from sms.objs.person import Person
from sms.objs.rubi import Rubi, RubiData
from sms.objs.stage import Stage
from sms.syss import messages as msg
from sms.types.asset import AssetType
from sms.utils import assertion
from sms.utils.log import logger


__all__ = (
        'asset_object_from',
        )


# Define Constants
PROC = 'ASSETS DATA CONV'

ELM_TAG = 'tag'

ELM_NAME = 'name'


# Main
def asset_object_from(data: str) -> SObject:
    assert isinstance(data, str)

    logger.debug(msg.PROC_START.format(proc=PROC))

    tmp = assertion.is_dict(yaml.safe_load(data))

    obj = None

    if str(AssetType.PERSON) in tmp:
        obj = Converter.to_person(tmp[str(AssetType.PERSON)])
    elif str(AssetType.STAGE) in tmp:
        obj = Converter.to_stage(tmp[str(AssetType.STAGE)])
    elif str(AssetType.ITEM) in tmp:
        obj = Converter.to_item(tmp[str(AssetType.ITEM)])
    elif str(AssetType.MOB) in tmp:
        obj = Converter.to_nametag(tmp)
    elif str(AssetType.TIME) in tmp:
        obj = Converter.to_nametag(tmp)
    elif str(AssetType.WORD) in tmp:
        obj = Converter.to_nametag(tmp)
    elif str(AssetType.RUBI) in tmp:
        obj = Converter.to_rubi(tmp[str(AssetType.RUBI)])
    else:
        logger.warning(
                msg.ERR_FAIL_INVALID_DATA_WITH_DATA.format(data=f"asset type: {PROC}"),
                tmp.keys())
        return None

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))

    return obj


# Processes
class Converter(object):

    def to_person(data: dict) -> Person:
        assert isinstance(data, dict)

        tag, name = _get_tag_and_name(data)
        person = Person(tag, name)
        if not _set_data_attr(person, data):
            return None
        else:
            return person

    def to_stage(data: dict) -> Stage:
        assert isinstance(data, dict)

        tag, name = _get_tag_and_name(data)
        stage = Stage(tag, name)
        if not _set_data_attr(stage, data):
            return None
        else:
            return stage

    def to_item(data: dict) -> Item:
        assert isinstance(data, dict)

        tag, name = _get_tag_and_name(data)
        item = Item(tag, name)
        if not _set_data_attr(item, data):
            return None
        else:
            return item

    def to_nametag(data: dict) -> NameTag:
        assert isinstance(data, dict)

        if str(AssetType.MOB) in data:
            return NameTag(NameTagType.MOB, data[str(AssetType.MOB)])
        elif str(AssetType.TIME) in data:
            return NameTag(NameTagType.TIME, data[str(AssetType.TIME)])
        elif str(AssetType.WORD) in data:
            return NameTag(NameTagType.WORD, data[str(AssetType.WORD)])
        else:
            logger.warning(msg.ERR_FAIL_UNKNOWN_DATA.format(data=f"tag type {data.keys()}: {PROC}"))
            return None

    def to_rubi(data: dict) -> Rubi:
        assert isinstance(data, dict)

        tmp = RubiData()

        for key, val in data.items():
            assert isinstance(key, str)
            assert isinstance(val, dict)
            tag = key
            name = data[tag][ELM_NAME]
            rubi = Rubi(tag, name)
            rubi.exclusions = data[tag]['exclusions']
            rubi.is_always = data[tag]['always']
            tmp.append(tag, rubi)

        return tmp


# Private Functions
def _get_tag_and_name(data: dict) -> tuple:
    assert isinstance(data, dict)

    return data[ELM_TAG], data[ELM_NAME]


def _safe_set_attr(obj: SObject, key: str, val: Any) -> bool:
    assert isinstance(obj, SObject)
    assert isinstance(key, str)

    if hasattr(obj, key):
        setattr(obj, key, val)
        return True
    else:
        return False


def _set_data_attr(obj: SObject, data: dict) -> bool:
    assert isinstance(obj, SObject)
    assert isinstance(data, dict)

    for key, val in data.items():
        if key in [ELM_TAG, ELM_NAME]:
            continue
        if not _safe_set_attr(obj, key, val):
            logger.warning(
                    msg.ERR_FAIL_CANNOT_WRITE_DATA_WITH_DATA.format(data=f"set '{key}'|'{val}': {PROC}"),
                    obj)
    return True
