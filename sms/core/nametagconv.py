"""Name tag converter module."""

# Official Libraries
import yaml


# My Modules
from sms.db.assets import AssetsDB
from sms.objs.baseobject import SObject
from sms.objs.item import Item
from sms.objs.nametag import NameTag, NameTagType
from sms.objs.person import Person
from sms.objs.rubi import Rubi, RubiData
from sms.objs.stage import Stage
from sms.syss import messages as msg
from sms.syss.paths import FILE_CONFIG
from sms.utils import assertion
from sms.utils.fileio import read_file
from sms.utils.log import logger
from sms.utils.strings import hankaku_to_zenkaku

__all__ = (
        'callingtags_from',
        'nametags_from',
        'rubitags_from',
        )


# Define Constants
PROC = 'NAME TAG CONV'

ELM_CONFIG = 'config'

ELM_MOBS = 'mobs'

ELM_NAME = 'name'

ELM_TYPE = 'type'

ELM_CLOCK = 'clock'


# Main
def callingtags_from(assets: AssetsDB) -> dict:
    assert isinstance(assets, AssetsDB)

    _PROC = f"{PROC}: calling tags"
    logger.debug(msg.PROC_START.format(proc=_PROC))

    tmp = {}

    for key, val in assets.data.items():
        assert isinstance(key, str)
        assert isinstance(val, SObject)
        if isinstance(val, Person):
            if not Converter.person_callings_of(tmp, val):
                logger.warning(
                        msg.ERR_FAIL_INVALID_DATA.format(
                            data=f"person '{val.tag} calling: {_PROC}'"))
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=_PROC))
    return tmp


def nametags_from(assets: AssetsDB) -> dict:
    assert isinstance(assets, AssetsDB)

    logger.debug(msg.PROC_START.format(proc=PROC))

    config = yaml.safe_load(read_file(FILE_CONFIG))
    if not config:
        logger.error(msg.ERR_FAIL_MISSING_DATA.format(data=f"config file: {PROC}"))
        return {}

    mob_num = config[ELM_CONFIG][ELM_MOBS]

    tmp = {}

    for key, val in assets.data.items():
        assert isinstance(key, str)
        assert isinstance(val, SObject)
        if isinstance(val, Person):
            if not Converter.person_names_of(tmp, val):
                logger.warning(
                        msg.ERR_FAIL_INVALID_DATA.format(
                            data=f"person '{val.tag}' name: {PROC}"))
        elif isinstance(val, Stage):
            if not Converter.stage_names_of(tmp, val):
                logger.warning(
                        msg.ERR_FAIL_INVALID_DATA.format(
                            data=f"stage '{val.tag}' name: {PROC}"))
        elif isinstance(val, Item):
            if not Converter.item_name_of(tmp, val):
                logger.warning(
                        msg.ERR_FAIL_INVALID_DATA.format(
                            data=f"item '{val.tag}' name: {PROC}"))
        elif isinstance(val, NameTag):
            if NameTagType.MOB is val.type:
                if not Converter.mob_name_of(tmp, val, mob_num):
                    logger.warning(
                            msg.ERR_FAIL_INVALID_DATA.format(
                                data=f"mob names: {PROC}"))
            elif NameTagType.TIME is val.type:
                if not Converter.time_name_of(tmp, val):
                    logger.warning(
                            msg.ERR_FAIL_INVALID_DATA.format(
                                data=f"time names: {PROC}"))
            elif NameTagType.WORD is val.type:
                if not Converter.word_name_of(tmp, val):
                    logger.warning(
                            msg.ERR_FAIL_INVALID_DATA.format(
                                data=f"word names: {PROC}"))
            else:
                continue
        elif isinstance(val, Rubi):
            continue
        else:
            continue

    logger.debug(msg.PROC_SUCCESS.format(proc=PROC))
    return tmp


def rubitags_from(assets: AssetsDB) -> RubiData:
    assert isinstance(assets, AssetsDB)

    tmp = {}

    for key, val in assets.data.items():
        assert isinstance(key, str)
        assert isinstance(val, SObject)
        if isinstance(val, RubiData):
            tmp = val
            break
        else:
            continue

    logger.debug(msg.PROC_MESSAGE.format(proc=f"conv rubi tags: {PROC}"))

    return tmp


def timeclocks_from(assets: AssetsDB) -> dict:
    assert isinstance(assets, AssetsDB)

    tmp = {}

    for key, val in assets.data.items():
        assert isinstance(key, str)
        assert isinstance(val, SObject)
        if isinstance(val, NameTag) and NameTagType.TIME is val.type:
            for tag, timeval in val.data.items():
                clock = timeval[ELM_CLOCK]
                tmp[tag] = clock
        else:
            continue

    logger.debug(msg.PROC_MESSAGE.format(proc=f"conv time clock tags: {PROC}"))

    return tmp


# Processes
class Converter(object):

    def person_callings_of(data: dict, obj: Person) -> bool:
        assert isinstance(data, dict)
        assert isinstance(obj, Person)

        calling = assertion.is_dict(obj.calling)
        calling['S'] = obj.name
        calling['M'] = calling['me'] if 'me' in calling else '私'

        data[obj.tag] = calling

        return True

    def person_names_of(data: dict, obj: Person) -> bool:
        assert isinstance(data, dict)
        assert isinstance(obj, Person)

        last, first = obj.fullname.split(',') if ',' in obj.fullname else ('', obj.name)

        data[obj.tag] = obj.name
        data[_add_prefix(obj.tag, 'n')] = obj.name
        data[_add_prefix(obj.tag, 'fn')] = first
        data[_add_prefix(obj.tag, 'ln')] = last
        data[_add_prefix(obj.tag, 'full')] = f"{last}{first}"
        data[_add_prefix(obj.tag, 'efull')] = f"{first}・{last}"

        return True

    def stage_names_of(data: dict, obj: Stage) -> bool:
        assert isinstance(data, dict)
        assert isinstance(obj, Stage)

        data[obj.tag] = obj.name
        data[_add_prefix(obj.tag, 't')] = obj.name

        return True

    def item_name_of(data: dict, obj: Item) -> bool:
        assert isinstance(data, dict)
        assert isinstance(obj, Item)

        data[obj.tag] = obj.name
        data[_add_prefix(obj.tag, 'i')] = obj.name

        return True

    def mob_name_of(data: dict, obj: NameTag, num: int) -> bool:
        assert isinstance(data, dict)
        assert isinstance(obj, NameTag)
        assert isinstance(num, int)

        for tag, val in obj.data.items():
            assert isinstance(tag, str)
            assert isinstance(val, dict)
            data[tag] = val[ELM_NAME]
            if 'mob' == val[ELM_TYPE]:
                for i in range(num):
                    data[f"{tag}{i}"] = val[ELM_NAME] + hankaku_to_zenkaku(str(i))

        return True

    def time_name_of(data: dict, obj: NameTag) -> bool:
        assert isinstance(data, dict)
        assert isinstance(obj, NameTag)

        for tag, val in obj.data.items():
            assert isinstance(tag, str)
            assert isinstance(val, dict)
            data[tag] = val[ELM_NAME]

        return True

    def word_name_of(data: dict, obj: NameTag) -> bool:
        assert isinstance(data, dict)
        assert isinstance(obj, NameTag)

        for tag, val in obj.data.items():
            assert isinstance(tag, str)
            assert isinstance(val, dict)
            data[tag] = val[ELM_NAME]

        return True


# Private Functions
def _add_prefix(base: str, prefix: str) -> str:
    assert isinstance(base, str)
    assert isinstance(prefix, str)

    return f"{prefix}_{base}"
