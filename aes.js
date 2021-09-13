var CryptoJS = CryptoJS || (function (Math, undefined) {
    var C = {};
    var C_lib = C.lib = {};
    var Base = C_lib.Base = (function () {
        function F() {};
        return {
            extend: function (overrides) {
                F.prototype = this;
                var subtype = new F();
                if (overrides) {
                    subtype.mixIn(overrides);
                }
                if (!subtype.hasOwnProperty('init') || this.init === subtype.init) {
                    subtype.init = function () {
                        subtype.$super.init.apply(this, arguments);
                    };
                }
                subtype.init.prototype = subtype;
                subtype.$super = this;
                return subtype;
            }, create: function () {
                var instance = this.extend();
                instance.init.apply(instance, arguments);
                return instance;
            }, init: function () {}, mixIn: function (properties) {
                for (var propertyName in properties) {
                    if (properties.hasOwnProperty(propertyName)) {
                        this[propertyName] = properties[propertyName];
                    }
                }
                if (properties.hasOwnProperty('toString')) {
                    this.toString = properties.toString;
                }
            }, clone: function () {
                return this.init.prototype.extend(this);
            }
        };
    }());
    var WordArray = C_lib.WordArray = Base.extend({
        init: function (words, sigBytes) {
            words = this.words = words || [];
            if (sigBytes != undefined) {
                this.sigBytes = sigBytes;
            } else {
                this.sigBytes = words.length * 4;
            }
        }, toString: function (encoder) {
            return (encoder || Hex).stringify(this);
        }, concat: function (wordArray) {
            var thisWords = this.words;
            var thatWords = wordArray.words;
            var thisSigBytes = this.sigBytes;
            var thatSigBytes = wordArray.sigBytes;
            this.clamp();
            if (thisSigBytes % 4) {
                for (var i = 0; i < thatSigBytes; i++) {
                    var thatByte = (thatWords[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
                    thisWords[(thisSigBytes + i) >>> 2] |= thatByte << (24 - ((thisSigBytes + i) % 4) * 8);
                }
            } else if (thatWords.length > 0xffff) {
                for (var i = 0; i < thatSigBytes; i += 4) {
                    thisWords[(thisSigBytes + i) >>> 2] = thatWords[i >>> 2];
                }
            } else {
                thisWords.push.apply(thisWords, thatWords);
            }
            this.sigBytes += thatSigBytes;
            return this;
        }, clamp: function () {
            var words = this.words;
            var sigBytes = this.sigBytes;
            words[sigBytes >>> 2] &= 0xffffffff << (32 - (sigBytes % 4) * 8);
            words.length = Math.ceil(sigBytes / 4);
        }, clone: function () {
            var clone = Base.clone.call(this);
            clone.words = this.words.slice(0);
            return clone;
        }, random: function (nBytes) {
            var words = [];
            var r = (function (m_w) {
                var m_w = m_w;
                var m_z = 0x3ade68b1;
                var mask = 0xffffffff;
                return function () {
                    m_z = (0x9069 * (m_z & 0xFFFF) + (m_z >> 0x10)) & mask;
                    m_w = (0x4650 * (m_w & 0xFFFF) + (m_w >> 0x10)) & mask;
                    var result = ((m_z << 0x10) + m_w) & mask;
                    result /= 0x100000000;
                    result += 0.5;
                    return result * (Math.random() > .5 ? 1 : -1);
                }
            });
            for (var i = 0, rcache; i < nBytes; i += 4) {
                var _r = r((rcache || Math.random()) * 0x100000000);
                rcache = _r() * 0x3ade67b7;
                words.push((_r() * 0x100000000) | 0);
            }
            return new WordArray.init(words, nBytes);
        }
    });
    var C_enc = C.enc = {};
    var Hex = C_enc.Hex = {
        stringify: function (wordArray) {
            var words = wordArray.words;
            var sigBytes = wordArray.sigBytes;
            var hexChars = [];
            for (var i = 0; i < sigBytes; i++) {
                var bite = (words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
                hexChars.push((bite >>> 4).toString(16));
                hexChars.push((bite & 0x0f).toString(16));
            }
            return hexChars.join('');
        }, parse: function (hexStr) {
            var hexStrLength = hexStr.length;
            var words = [];
            for (var i = 0; i < hexStrLength; i += 2) {
                words[i >>> 3] |= parseInt(hexStr.substr(i, 2), 16) << (24 - (i % 8) * 4);
            }
            return new WordArray.init(words, hexStrLength / 2);
        }
    };
    var Latin1 = C_enc.Latin1 = {
        stringify: function (wordArray) {
            var words = wordArray.words;
            var sigBytes = wordArray.sigBytes;
            var latin1Chars = [];
            for (var i = 0; i < sigBytes; i++) {
                var bite = (words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
                latin1Chars.push(String.fromCharCode(bite));
            }
            return latin1Chars.join('');
        }, parse: function (latin1Str) {
            var latin1StrLength = latin1Str.length;
            var words = [];
            for (var i = 0; i < latin1StrLength; i++) {
                words[i >>> 2] |= (latin1Str.charCodeAt(i) & 0xff) << (24 - (i % 4) * 8);
            }
            return new WordArray.init(words, latin1StrLength);
        }
    };
    var Utf8 = C_enc.Utf8 = {
        stringify: function (wordArray) {
            try {
                return decodeURIComponent(escape(Latin1.stringify(wordArray)));
            } catch (e) {
                throw new Error('Malformed UTF-8 data');
            }
        }, parse: function (utf8Str) {
            return Latin1.parse(unescape(encodeURIComponent(utf8Str)));
        }
    };
    var BufferedBlockAlgorithm = C_lib.BufferedBlockAlgorithm = Base.extend({
        reset: function () {
            this._data = new WordArray.init();
            this._nDataBytes = 0;
        }, _append: function (data) {
            if (typeof data == 'string') {
                data = Utf8.parse(data);
            }
            this._data.concat(data);
            this._nDataBytes += data.sigBytes;
        }, _process: function (doFlush) {
            var data = this._data;
            var dataWords = data.words;
            var dataSigBytes = data.sigBytes;
            var blockSize = this.blockSize;
            var blockSizeBytes = blockSize * 4;
            var nBlocksReady = dataSigBytes / blockSizeBytes;
            if (doFlush) {
                nBlocksReady = Math.ceil(nBlocksReady);
            } else {
                nBlocksReady = Math.max((nBlocksReady | 0) - this._minBufferSize, 0);
            }
            var nWordsReady = nBlocksReady * blockSize;
            var nBytesReady = Math.min(nWordsReady * 4, dataSigBytes);
            if (nWordsReady) {
                for (var offset = 0; offset < nWordsReady; offset += blockSize) {
                    this._doProcessBlock(dataWords, offset);
                }
                var processedWords = dataWords.splice(0, nWordsReady);
                data.sigBytes -= nBytesReady;
            }
            return new WordArray.init(processedWords, nBytesReady);
        }, clone: function () {
            var clone = Base.clone.call(this);
            clone._data = this._data.clone();
            return clone;
        }, _minBufferSize: 0
    });
    var Hasher = C_lib.Hasher = BufferedBlockAlgorithm.extend({
        cfg: Base.extend(),
        init: function (cfg) {
            this.cfg = this.cfg.extend(cfg);
            this.reset();
        }, reset: function () {
            BufferedBlockAlgorithm.reset.call(this);
            this._doReset();
        }, update: function (messageUpdate) {
            this._append(messageUpdate);
            this._process();
            return this;
        }, finalize: function (messageUpdate) {
            if (messageUpdate) {
                this._append(messageUpdate);
            }
            var hash = this._doFinalize();
            return hash;
        }, blockSize: 512 / 32,
        _createHelper: function (hasher) {
            return function (message, cfg) {
                return new hasher.init(cfg).finalize(message);
            };
        }, _createHmacHelper: function (hasher) {
            return function (message, key) {
                return new C_algo.HMAC.init(hasher, key).finalize(message);
            };
        }
    });
    var C_algo = C.algo = {};
    return C;
}(Math));

(function () {
    var C = CryptoJS;
    var C_lib = C.lib;
    var WordArray = C_lib.WordArray;
    var C_enc = C.enc;
    var Base64 = C_enc.Base64 = {
        stringify: function (wordArray) {
            var words = wordArray.words;
            var sigBytes = wordArray.sigBytes;
            var map = this._map;
            wordArray.clamp();
            var base64Chars = [];
            for (var i = 0; i < sigBytes; i += 3) {
                var byte1 = (words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
                var byte2 = (words[(i + 1) >>> 2] >>> (24 - ((i + 1) % 4) * 8)) & 0xff;
                var byte3 = (words[(i + 2) >>> 2] >>> (24 - ((i + 2) % 4) * 8)) & 0xff;
                var triplet = (byte1 << 16) | (byte2 << 8) | byte3;
                for (var j = 0;
                    (j < 4) && (i + j * 0.75 < sigBytes); j++) {
                    base64Chars.push(map.charAt((triplet >>> (6 * (3 - j))) & 0x3f));
                }
            }
            var paddingChar = map.charAt(64);
            if (paddingChar) {
                while (base64Chars.length % 4) {
                    base64Chars.push(paddingChar);
                }
            }
            return base64Chars.join('');
        }, parse: function (base64Str) {
            var base64StrLength = base64Str.length;
            var map = this._map;
            var reverseMap = this._reverseMap;
            if (!reverseMap) {
                reverseMap = this._reverseMap = [];
                for (var j = 0; j < map.length; j++) {
                    reverseMap[map.charCodeAt(j)] = j;
                }
            }
            var paddingChar = map.charAt(64);
            if (paddingChar) {
                var paddingIndex = base64Str.indexOf(paddingChar);
                if (paddingIndex !== -1) {
                    base64StrLength = paddingIndex;
                }
            }
            return parseLoop(base64Str, base64StrLength, reverseMap);
        }, _map: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    };
    function parseLoop(base64Str, base64StrLength, reverseMap) {
        var words = [];
        var nBytes = 0;
        for (var i = 0; i < base64StrLength; i++) {
            if (i % 4) {
                var bits1 = reverseMap[base64Str.charCodeAt(i - 1)] << ((i % 4) * 2);
                var bits2 = reverseMap[base64Str.charCodeAt(i)] >>> (6 - (i % 4) * 2);
                words[nBytes >>> 2] |= (bits1 | bits2) << (24 - (nBytes % 4) * 8);
                nBytes++;
            }
        }
        return WordArray.create(words, nBytes);
    }
}());

CryptoJS.lib.Cipher || (function (undefined) {
    var C = CryptoJS;
    var C_lib = C.lib;
    var Base = C_lib.Base;
    var WordArray = C_lib.WordArray;
    var BufferedBlockAlgorithm = C_lib.BufferedBlockAlgorithm;
    var C_enc = C.enc;
    var Utf8 = C_enc.Utf8;
    var Base64 = C_enc.Base64;
    var C_algo = C.algo;
    var EvpKDF = C_algo.EvpKDF;
    var Cipher = C_lib.Cipher = BufferedBlockAlgorithm.extend({
        cfg: Base.extend(),
        createEncryptor: function (key, cfg) {
            return this.create(this._ENC_XFORM_MODE, key, cfg);
        }, createDecryptor: function (key, cfg) {
            return this.create(this._DEC_XFORM_MODE, key, cfg);
        }, init: function (xformMode, key, cfg) {
            this.cfg = this.cfg.extend(cfg);
            this._xformMode = xformMode;
            this._key = key;
            this.reset();
        }, reset: function () {
            BufferedBlockAlgorithm.reset.call(this);
            this._doReset();
        }, process: function (dataUpdate) {
            this._append(dataUpdate);
            return this._process();
        }, finalize: function (dataUpdate) {
            if (dataUpdate) {
                this._append(dataUpdate);
            }
            var finalProcessedData = this._doFinalize();
            return finalProcessedData;
        }, keySize: 128 / 32,
        ivSize: 128 / 32,
        _ENC_XFORM_MODE: 1,
        _DEC_XFORM_MODE: 2,
        _createHelper: (function () {
            function selectCipherStrategy(key) {
                if (typeof key == 'string') {
                    return PasswordBasedCipher;
                } else {
                    return SerializableCipher;
                }
            }
            return function (cipher) {
                return {
                    encrypt: function (message, key, cfg) {
                        return selectCipherStrategy(key).encrypt(cipher, message, key, cfg);
                    }, decrypt: function (ciphertext, key, cfg) {
                        return selectCipherStrategy(key).decrypt(cipher, ciphertext, key, cfg);
                    }
                };
            };
        }())
    });
    var StreamCipher = C_lib.StreamCipher = Cipher.extend({
        _doFinalize: function () {
            var finalProcessedBlocks = this._process(!!'flush');
            return finalProcessedBlocks;
        }, blockSize: 1
    });
    var C_mode = C.mode = {};
    var BlockCipherMode = C_lib.BlockCipherMode = Base.extend({
        createEncryptor: function (cipher, iv) {
            return this.Encryptor.create(cipher, iv);
        }, createDecryptor: function (cipher, iv) {
            return this.Decryptor.create(cipher, iv);
        }, init: function (cipher, iv) {
            this._cipher = cipher;
            this._iv = iv;
        }
    });
    var CBC = C_mode.CBC = (function () {
        var CBC = BlockCipherMode.extend();
        CBC.Encryptor = CBC.extend({
            processBlock: function (words, offset) {
                var cipher = this._cipher;
                var blockSize = cipher.blockSize;
                xorBlock.call(this, words, offset, blockSize);
                cipher.encryptBlock(words, offset);
                this._prevBlock = words.slice(offset, offset + blockSize);
            }
        });
        CBC.Decryptor = CBC.extend({
            processBlock: function (words, offset) {
                var cipher = this._cipher;
                var blockSize = cipher.blockSize;
                var thisBlock = words.slice(offset, offset + blockSize);
                cipher.decryptBlock(words, offset);
                xorBlock.call(this, words, offset, blockSize);
                this._prevBlock = thisBlock;
            }
        });

        function xorBlock(words, offset, blockSize) {
            var iv = this._iv;
            if (iv) {
                var block = iv;
                this._iv = undefined;
            } else {
                var block = this._prevBlock;
            }
            for (var i = 0; i < blockSize; i++) {
                words[offset + i] ^= block[i];
            }
        }
        return CBC;
    }());
    var C_pad = C.pad = {};
    var Pkcs7 = C_pad.Pkcs7 = {
        pad: function (data, blockSize) {
            var blockSizeBytes = blockSize * 4;
            var nPaddingBytes = blockSizeBytes - data.sigBytes % blockSizeBytes;
            var paddingWord = (nPaddingBytes << 24) | (nPaddingBytes << 16) | (nPaddingBytes << 8) | nPaddingBytes;
            var paddingWords = [];
            for (var i = 0; i < nPaddingBytes; i += 4) {
                paddingWords.push(paddingWord);
            }
            var padding = WordArray.create(paddingWords, nPaddingBytes);
            data.concat(padding);
        }, unpad: function (data) {
            var nPaddingBytes = data.words[(data.sigBytes - 1) >>> 2] & 0xff;
            data.sigBytes -= nPaddingBytes;
        }
    };
    var BlockCipher = C_lib.BlockCipher = Cipher.extend({
        cfg: Cipher.cfg.extend({
            mode: CBC,
            padding: Pkcs7
        }),
        reset: function () {
            Cipher.reset.call(this);
            var cfg = this.cfg;
            var iv = cfg.iv;
            var mode = cfg.mode;
            if (this._xformMode == this._ENC_XFORM_MODE) {
                var modeCreator = mode.createEncryptor;
            } else {
                var modeCreator = mode.createDecryptor;
                this._minBufferSize = 1;
            } if (this._mode && this._mode.__creator == modeCreator) {
                this._mode.init(this, iv && iv.words);
            } else {
                this._mode = modeCreator.call(mode, this, iv && iv.words);
                this._mode.__creator = modeCreator;
            }
        }, _doProcessBlock: function (words, offset) {
            this._mode.processBlock(words, offset);
        }, _doFinalize: function () {
            var padding = this.cfg.padding;
            if (this._xformMode == this._ENC_XFORM_MODE) {
                padding.pad(this._data, this.blockSize);
                var finalProcessedBlocks = this._process(!!'flush');
            } else {
                var finalProcessedBlocks = this._process(!!'flush');
                padding.unpad(finalProcessedBlocks);
            }
            return finalProcessedBlocks;
        }, blockSize: 128 / 32
    });
    var CipherParams = C_lib.CipherParams = Base.extend({
        init: function (cipherParams) {
            this.mixIn(cipherParams);
        }, toString: function (formatter) {
            return (formatter || this.formatter).stringify(this);
        }
    });
    var C_format = C.format = {};
    var OpenSSLFormatter = C_format.OpenSSL = {
        stringify: function (cipherParams) {
            var ciphertext = cipherParams.ciphertext;
            var salt = cipherParams.salt;
            if (salt) {
                var wordArray = WordArray.create([0x53616c74, 0x65645f5f]).concat(salt).concat(ciphertext);
            } else {
                var wordArray = ciphertext;
            }
            return wordArray.toString(Base64);
        }, parse: function (openSSLStr) {
            var ciphertext = Base64.parse(openSSLStr);
            var ciphertextWords = ciphertext.words;
            if (ciphertextWords[0] == 0x53616c74 && ciphertextWords[1] == 0x65645f5f) {
                var salt = WordArray.create(ciphertextWords.slice(2, 4));
                ciphertextWords.splice(0, 4);
                ciphertext.sigBytes -= 16;
            }
            return CipherParams.create({
                ciphertext: ciphertext,
                salt: salt
            });
        }
    };
    var SerializableCipher = C_lib.SerializableCipher = Base.extend({
        cfg: Base.extend({
            format: OpenSSLFormatter
        }),
        encrypt: function (cipher, message, key, cfg) {
            cfg = this.cfg.extend(cfg);
            var encryptor = cipher.createEncryptor(key, cfg);
            var ciphertext = encryptor.finalize(message);
            var cipherCfg = encryptor.cfg;
            return CipherParams.create({
                ciphertext: ciphertext,
                key: key,
                iv: cipherCfg.iv,
                algorithm: cipher,
                mode: cipherCfg.mode,
                padding: cipherCfg.padding,
                blockSize: cipher.blockSize,
                formatter: cfg.format
            });
        }, decrypt: function (cipher, ciphertext, key, cfg) {
            cfg = this.cfg.extend(cfg);
            ciphertext = this._parse(ciphertext, cfg.format);
            var plaintext = cipher.createDecryptor(key, cfg).finalize(ciphertext.ciphertext);
            return plaintext;
        }, _parse: function (ciphertext, format) {
            if (typeof ciphertext == 'string') {
                return format.parse(ciphertext, this);
            } else {
                return ciphertext;
            }
        }
    });
    var C_kdf = C.kdf = {};
    var OpenSSLKdf = C_kdf.OpenSSL = {
        execute: function (password, keySize, ivSize, salt) {
            if (!salt) {
                salt = WordArray.random(64 / 8);
            }
            var key = EvpKDF.create({
                keySize: keySize + ivSize
            }).compute(password, salt);
            var iv = WordArray.create(key.words.slice(keySize), ivSize * 4);
            key.sigBytes = keySize * 4;
            return CipherParams.create({
                key: key,
                iv: iv,
                salt: salt
            });
        }
    };
    var PasswordBasedCipher = C_lib.PasswordBasedCipher = SerializableCipher.extend({
        cfg: SerializableCipher.cfg.extend({
            kdf: OpenSSLKdf
        }),
        encrypt: function (cipher, message, password, cfg) {
            cfg = this.cfg.extend(cfg);
            var derivedParams = cfg.kdf.execute(password, cipher.keySize, cipher.ivSize);
            cfg.iv = derivedParams.iv;
            var ciphertext = SerializableCipher.encrypt.call(this, cipher, message, derivedParams.key, cfg);
            ciphertext.mixIn(derivedParams);
            return ciphertext;
        }, decrypt: function (cipher, ciphertext, password, cfg) {
            cfg = this.cfg.extend(cfg);
            ciphertext = this._parse(ciphertext, cfg.format);
            var derivedParams = cfg.kdf.execute(password, cipher.keySize, cipher.ivSize, ciphertext.salt);
            cfg.iv = derivedParams.iv;
            var plaintext = SerializableCipher.decrypt.call(this, cipher, ciphertext, derivedParams.key, cfg);
            return plaintext;
        }
    });
}());

(function () {
    var C = CryptoJS;
    var C_lib = C.lib;
    var BlockCipher = C_lib.BlockCipher;
    var C_algo = C.algo;
    var SBOX = [];
    var INV_SBOX = [];
    var SUB_MIX_0 = [];
    var SUB_MIX_1 = [];
    var SUB_MIX_2 = [];
    var SUB_MIX_3 = [];
    var INV_SUB_MIX_0 = [];
    var INV_SUB_MIX_1 = [];
    var INV_SUB_MIX_2 = [];
    var INV_SUB_MIX_3 = [];
    (function () {
        var d = [];
        for (var i = 0; i < 256; i++) {
            if (i < 128) {
                d[i] = i << 1;
            } else {
                d[i] = (i << 1) ^ 0x11b;
            }
        }
        var x = 0;
        var xi = 0;
        for (var i = 0; i < 256; i++) {
            var sx = xi ^ (xi << 1) ^ (xi << 2) ^ (xi << 3) ^ (xi << 4);
            sx = (sx >>> 8) ^ (sx & 0xff) ^ 0x63;
            SBOX[x] = sx;
            INV_SBOX[sx] = x;
            var x2 = d[x];
            var x4 = d[x2];
            var x8 = d[x4];
            var t = (d[sx] * 0x101) ^ (sx * 0x1010100);
            SUB_MIX_0[x] = (t << 24) | (t >>> 8);
            SUB_MIX_1[x] = (t << 16) | (t >>> 16);
            SUB_MIX_2[x] = (t << 8) | (t >>> 24);
            SUB_MIX_3[x] = t;
            var t = (x8 * 0x1010101) ^ (x4 * 0x10001) ^ (x2 * 0x101) ^ (x * 0x1010100);
            INV_SUB_MIX_0[sx] = (t << 24) | (t >>> 8);
            INV_SUB_MIX_1[sx] = (t << 16) | (t >>> 16);
            INV_SUB_MIX_2[sx] = (t << 8) | (t >>> 24);
            INV_SUB_MIX_3[sx] = t;
            if (!x) {
                x = xi = 1;
            } else {
                x = x2 ^ d[d[d[x8 ^ x2]]];
                xi ^= d[d[xi]];
            }
        }
    }());
    var RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36];
    var AES = C_algo.AES = BlockCipher.extend({
        _doReset: function () {
            if (this._nRounds && this._keyPriorReset === this._key) {
                return;
            }
            var key = this._keyPriorReset = this._key;
            var keyWords = key.words;
            var keySize = key.sigBytes / 4;
            var nRounds = this._nRounds = keySize + 6;
            var ksRows = (nRounds + 1) * 4;
            var keySchedule = this._keySchedule = [];
            for (var ksRow = 0; ksRow < ksRows; ksRow++) {
                if (ksRow < keySize) {
                    keySchedule[ksRow] = keyWords[ksRow];
                } else {
                    var t = keySchedule[ksRow - 1];
                    if (!(ksRow % keySize)) {
                        t = (t << 8) | (t >>> 24);
                        t = (SBOX[t >>> 24] << 24) | (SBOX[(t >>> 16) & 0xff] << 16) | (SBOX[(t >>> 8) & 0xff] << 8) | SBOX[t & 0xff];
                        t ^= RCON[(ksRow / keySize) | 0] << 24;
                    } else if (keySize > 6 && ksRow % keySize == 4) {
                        t = (SBOX[t >>> 24] << 24) | (SBOX[(t >>> 16) & 0xff] << 16) | (SBOX[(t >>> 8) & 0xff] << 8) | SBOX[t & 0xff];
                    }
                    keySchedule[ksRow] = keySchedule[ksRow - keySize] ^ t;
                }
            }
            var invKeySchedule = this._invKeySchedule = [];
            for (var invKsRow = 0; invKsRow < ksRows; invKsRow++) {
                var ksRow = ksRows - invKsRow;
                if (invKsRow % 4) {
                    var t = keySchedule[ksRow];
                } else {
                    var t = keySchedule[ksRow - 4];
                } if (invKsRow < 4 || ksRow <= 4) {
                    invKeySchedule[invKsRow] = t;
                } else {
                    invKeySchedule[invKsRow] = INV_SUB_MIX_0[SBOX[t >>> 24]] ^ INV_SUB_MIX_1[SBOX[(t >>> 16) & 0xff]] ^ INV_SUB_MIX_2[SBOX[(t >>> 8) & 0xff]] ^ INV_SUB_MIX_3[SBOX[t & 0xff]];
                }
            }
        }, encryptBlock: function (M, offset) {
            this._doCryptBlock(M, offset, this._keySchedule, SUB_MIX_0, SUB_MIX_1, SUB_MIX_2, SUB_MIX_3, SBOX);
        }, decryptBlock: function (M, offset) {
            var t = M[offset + 1];
            M[offset + 1] = M[offset + 3];
            M[offset + 3] = t;
            this._doCryptBlock(M, offset, this._invKeySchedule, INV_SUB_MIX_0, INV_SUB_MIX_1, INV_SUB_MIX_2, INV_SUB_MIX_3, INV_SBOX);
            var t = M[offset + 1];
            M[offset + 1] = M[offset + 3];
            M[offset + 3] = t;
        }, _doCryptBlock: function (M, offset, keySchedule, SUB_MIX_0, SUB_MIX_1, SUB_MIX_2, SUB_MIX_3, SBOX) {
            var nRounds = this._nRounds;
            var s0 = M[offset] ^ keySchedule[0];
            var s1 = M[offset + 1] ^ keySchedule[1];
            var s2 = M[offset + 2] ^ keySchedule[2];
            var s3 = M[offset + 3] ^ keySchedule[3];
            var ksRow = 4;
            for (var round = 1; round < nRounds; round++) {
                var t0 = SUB_MIX_0[s0 >>> 24] ^ SUB_MIX_1[(s1 >>> 16) & 0xff] ^ SUB_MIX_2[(s2 >>> 8) & 0xff] ^ SUB_MIX_3[s3 & 0xff] ^ keySchedule[ksRow++];
                var t1 = SUB_MIX_0[s1 >>> 24] ^ SUB_MIX_1[(s2 >>> 16) & 0xff] ^ SUB_MIX_2[(s3 >>> 8) & 0xff] ^ SUB_MIX_3[s0 & 0xff] ^ keySchedule[ksRow++];
                var t2 = SUB_MIX_0[s2 >>> 24] ^ SUB_MIX_1[(s3 >>> 16) & 0xff] ^ SUB_MIX_2[(s0 >>> 8) & 0xff] ^ SUB_MIX_3[s1 & 0xff] ^ keySchedule[ksRow++];
                var t3 = SUB_MIX_0[s3 >>> 24] ^ SUB_MIX_1[(s0 >>> 16) & 0xff] ^ SUB_MIX_2[(s1 >>> 8) & 0xff] ^ SUB_MIX_3[s2 & 0xff] ^ keySchedule[ksRow++];
                s0 = t0;
                s1 = t1;
                s2 = t2;
                s3 = t3;
            }
            var t0 = ((SBOX[s0 >>> 24] << 24) | (SBOX[(s1 >>> 16) & 0xff] << 16) | (SBOX[(s2 >>> 8) & 0xff] << 8) | SBOX[s3 & 0xff]) ^ keySchedule[ksRow++];
            var t1 = ((SBOX[s1 >>> 24] << 24) | (SBOX[(s2 >>> 16) & 0xff] << 16) | (SBOX[(s3 >>> 8) & 0xff] << 8) | SBOX[s0 & 0xff]) ^ keySchedule[ksRow++];
            var t2 = ((SBOX[s2 >>> 24] << 24) | (SBOX[(s3 >>> 16) & 0xff] << 16) | (SBOX[(s0 >>> 8) & 0xff] << 8) | SBOX[s1 & 0xff]) ^ keySchedule[ksRow++];
            var t3 = ((SBOX[s3 >>> 24] << 24) | (SBOX[(s0 >>> 16) & 0xff] << 16) | (SBOX[(s1 >>> 8) & 0xff] << 8) | SBOX[s2 & 0xff]) ^ keySchedule[ksRow++];
            M[offset] = t0;
            M[offset + 1] = t1;
            M[offset + 2] = t2;
            M[offset + 3] = t3;
        }, keySize: 256 / 32
    });
    C.AES = BlockCipher._createHelper(AES);
}());



function AES_Encrypt(word) {
    var srcs = CryptoJS.enc.Utf8.parse(word);
    var encrypted = CryptoJS.AES.encrypt(srcs, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return CryptoJS.enc.Hex.stringify(CryptoJS.enc.Base64.parse(encrypted.toString()));
}

function AES_Decrypt(word) {
    var srcs = CryptoJS.enc.Base64.stringify(CryptoJS.enc.Hex.parse(word));
    var decrypt = CryptoJS.AES.decrypt(srcs, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return decrypt.toString(CryptoJS.enc.Utf8);
}

//var key = CryptoJS.enc.Utf8.parse("jo8j9wGw%6HbxfFn");
//var iv = CryptoJS.enc.Utf8.parse("0123456789ABCDEF");

var key = CryptoJS.enc.Hex.parse("4587dc9b6a7c3e9ef3b920f994edc3a210c460977528138d41e58b9b02c94ffd");
var iv = CryptoJS.enc.Hex.parse("bbed223ead243413369c62eefa760906");
var data='d58cd0d7d981d6d547793fa375c91065ae2db015f24a61a20abe69c663bbcf3bc4a21abe16dcfa50128c7d8efdc72ab1039a0d854e1c49eb81f2149855428a9afce4a8ed2190f3af36da75e659e64957a00711bffb71b8a852a134f613735ce8c6016f13f985bf7c2e6468e376d7fcba32fe0041730676e962e56a4b7876b8ba689d240245d9c730efda130ecf2530c92700931f0d641a4969006a514f480512ce1d109e2389e87a30e6b9538f711cf5d05b2b9dadf92cbb7261cd796c50b1619a3e6842ae61f0b98f19d5b2c063fdd86507bba14849c628f4e5f9348bde31e7da5d04270c4677c803c9152cbe1c7e609fed305b0f6a8ad704b6d42c5f8f4d334b1e964da409da4e8e9f0b3e5b206703aad3ce7870400be6557951d52128a8b3933636f5d83222e911a5eebfaeb243c796d8a20d2ac8b1c03d2ab99f154e1880c6a0a369ba51b1caa47a1f3cc13a6c0719d724c7e48e694a041cab2c264b937378561509010a778ef7879f8bcd795a07e52bdc67bceb4fa57463841e345372970cb6b6d3a4568db615de77e7e1189b7b14a9aa64f736dadfbbfb345260c87647238f4fcb6a1718f12dec766b96f27806ce86ba350f8762c9bb572072e345994236da5c4dbba81152ff3957230f571b46ef209829aee4240af3ee3bc5f07c11188b4149b3989fc76ddd67db61a89f5f86c1c4094670c6bd3bcf2032cd1f7abb0d71b15d05c73c0d9c1125f1bf1895c24efa4657bec89723077775d8eeeb2816c0cd6c4d56038f917d836db576bdd1fe4f7c5f855ee3be818bb86dc76d42c6b4b842ca6ced72a3b3299c2a5697e1a303267f5e7d929b22a963f01f4f8bd00eae0b8e04aa8438fe182c91349e58bc6a01528baef1fef4b5191b5a7fbab2e13e1b2768730c4a164b9939b1f2a108dfe8b3ba166d2cf02d1a8c615a01f84dee4703a1b7c8efbaf1dbc3a26afbc14bb50dd3fb3afce474751ce31297117397942f2a99c866e1cb59e27a938932115617127ead904b3053bae1607faf09ecd9d4caafaa78eb909722c8ae545d1f4598225c904100fde0ac48cae7ab56c001bde0a0f1ac05a4232502655da0cc05897dd11ae7b72bd8ce70be5b5f0b1b7a303ffd234ec9b6ff373c71cfeeecd6680f703c314b01ec203b66ccfcb80de9d7158cb9ecce0764a85dd6c9c72ce22118a10569abe98354ac4e0311df64f99fb2f07d71027f7cf52ebf4d6f88d86d5ccea9130d30a8e3b0ec432134bf8c649167573c8bd36204ffb59b9f1a4d617e7a3acc8a0e6b78d576e15262f892b199c5536ca86aeef6f4ed52cf6445f8c03ca31577a652d1aa2baf2f2cac6b1115d783fa09fb6455ce3caa13699bc8b8b6009c7aee87ac393af1552cc265cb4620731f6aad597d7f375a5d192aac9d7bed13382e702d2e44586ce6d8029e40ccafbd6f59dda3d0481324b9e374379e3783f891bca137c0d48f0078b82c626441524c3078d17bf1b63ae88ee14629c80352b9a7b9d8873b75fc88dd1199d38c13d8fcfc7a34fd3e6e2b61f22d7ae95578fd7f674516a6a9208066bbe460c2b5a5c76fa1bd8cae670f3be221d133827c71c80e2d34905d4878c95ea558e63ca1b5c5084c3af42448599fac130132d9c0314869fb2db34ad72dac5f9353bea4b6454fb4089330044bfd0b0ddc9fe97e6bb335644b6ad94226da5e0f7fa650b22a62e3703d77f9326fbed6fa3d64644cbfc5df55123d8fdf0da5caeb843b0b6d7b3c8e56761315ab07c8a055ca67a13760c1e5f2c98c01b5da98a9ca6adce470153604dbd90e441f561d554ec940f434f6158e89f0a7ee5eea772e8919c5486454de2c9aab35959e312669666c1248b5675b76be4fcf8befd9ba7b8a34f747171f17a2a754087f71b20e5c145804c535c80070a48100fa555ae10832cd9963baf5dfbfabbe267f0c166a4dcd3d6234ba145fe3011cba18b13725ff7b745bf0684ddee849b80834a9b8a9c0750e3b0e480324bb4d11e701709f84fbec81299d053fdbac603b724b6866ccf0d800ac8d87737b60801e459c478259c1e3f787bf6047d8139dca1cf48b445e29bd29001f9d8da835f2e93d5a31d115e71d0cd8f1dbb625de9d89e9e4dc4401fb9ea974d9e8bada2c111d368c26eaad8f943c73b99010e82e1d195611a0157dd4bb06c3aff35afc320286dea72fb9cb714e5b756db600a1276d74324a66b4affe3307d9f54c3d175fe4067aec6af0aafe849e064226ca1f10b0b53b6fd288d7d6791128ed2873b55ba2bd3d809cd976e79e1bb32985c8c05a93f0c8aa976d59b49fb02daee5cfaa014a899476667623271eb62c348e6656b5488437904f2c26eea1dcc518a2349326a00292bdbfe8687baf8c76d17dfebfd117052ff9e1ec60d6886b958bf95f7f1b23390ed1c8cc54e8539c2dfc66fcde182b66bfcfa3f9d8688f7a2d21a8ffa2526f79a827985fad33770bb12f472642b0d9c8064960ef95ec8af382d67095f6113900bb886dcb9c33ac923f56d738893817f8028267ed61389f15b3bad7bf37f223d2c0827a9172c8167f5d473c12cadb05d59281547404f05de535ce597c5beedaa89b6416ce81323eacfa8eb406f79db08f279f5944ee3411356d8784f68dc06455c572e88b195216da6a1e0f3107fb58a06a36359f6d3f33769c3f8ad0bb852c6e7a246c9dfea065e7237f295159b7578fc6a5e3d5dde73afbfe1c6aa263851f3af83eaf8f83cfd40d0943dec0abbd916cc0455d57ebe82085638ba6d31f98e97c7b4bdb7df315e6ccad6a34fea4e44b8c9e78502eadc3a0070b0c21648f567f943c46148b0aa7a37d29ea69c7835b9f9465e129298670618d0670f0edd69252cacd3095073343ab68fd90d2ed2f0c03b01af748162ce32efe91de76ff684e14aa09922bf6973fc7a9a46eb027c213358ffc9d812a4a1a759f683310e143df93bd3abab60bc8f10e5f8c45daf6794163dc8d6b8c4594c726812299c7817e8ad855e870c8641b362bbec58b46d3f2576bc47b4da4cf90f947b1087ac2d93f16b6791be7eaeda95cd44e3d4ec81cddceb9f26ccb2082ff03d2c7c8f79e7327e50712b68b40738213d578bcaa289bbeb17302d9ba0f82755544a9ebf5e56fab6bcd8b141b57885cce6777ce249bcf40dad7e66df8948246cc2d8405cb9e434eb52157d48f9cfbec920832b28021fba2756218ead100f295156ad3810d63f5353b646562804584a17e3c8d29b410d38e781cc5f9d2a14068b432dfea9cd1db71957f48c6914f1d4ec5ccca6ba7375b34c90c3e8129b444e7a2ceb47271485d767baf9f77e91dc0252ab8fcfd951cc7e1eb0634f710d393be1ffe284ce036ba03e74e40ed293c749ad19a826febfdd84c0abe47e552a4b5e4df25a753e6d3dd935c074f080c571e472457e0f8cd1ac3f940aa0d7b82b632d2fa504e4c533fb49ad9609648af35b3f7968a90d42719443ff6ab43771a435778f3272ae7051808cbf291c1b2f4409a3ad65c0dc54150b93819a4329c4b848568b3c9d8c548ce1e4264326ff85ddde3c57458b5cb38a33706df6502d9089e2e832c5c529f5afc51dd57d67a36e8dacd51928c47046201d598ee0fb6c7dc4894ae0bfa9c3b932dffccdeed29d81d699e6f98cbf219aa74755b390c198973a3df78547f487075ff29d2b8ed0ed7a057b7b48f39b80d0b282970085538daf130579cba8c8a8af88bedec0f000c554a5c3cbe837e7a4df0f2639fc0d6f49a505552ca330edfeabae4e45fcc1707c26b0f1bca0334f08bcab3a21afbc9b1c6c2a08ef3be20d72838a104952bcce2c9e35387ee68575f9d6775529a5bea2592fe58a923b6be3515c956dca99a66259cdccc3c2286e5ac213188d1c031f55dde531880070111bf2aa8cfbfe35eb56440435864cdfdd37c84a48f79376ef56cc6307f6418d8e746737ae666c813dd608dd97b4c4d019a89bc4803612528489f8016759849ffbbfbd036ed9bde06d013733e3824ab2be72025883757f7d54fe4ffd275f0f10df35c7e03669e15c5f5b5fd6cbf5d421b3aca466147a803a86dca2af88befc4e9bfa04ce1e3c167b49edf90ee88ebc45caa9974bc829688141c07db84014878afc9b8dc0dac201345728b2af7899c6ef2a7b76ef20083602eea23a076b75a714619baf0f1b451b00a5cec088efe39a5e499c83d3524c95ceaae055559c96ef1eab4674191d7ab3cd66eecd9f5f86790fbe57a30f2281314129f38dadca23c76009acf7a18fbb8812337b422c2db6efe476d0076ece2fc168abe7d886e9c3dbdb4a47c3f8892c62ae7005e018b6bb22d67ee412f17c15a107b38557a5900a86986d5da922452079d765ba1b28b6f4f227610352c49eb2e4b709503594435927cc1acd8cada87dcf1782a54083fd21f9be8df9d549e631e6d5eec6fca57176dd918b4f46d8190c805201d25b2c33e82bed2dfe274f70019f793e3b18ba4e6f815143e90ca5c883257105bab2944b0e4bbad5cfd3126716f09a0bfe0e7f861f88431445de025c3f1fa52936c8effdd413eba1e433e73a75d4d3f9b12c30b441c7022ba0419b9e7859e447e5572b4645d392392ae9c5f0c712b08b7bf7f96cec10ba74676ed54e8f7eb146027d6b3c5db2378928e01191881dbceaebb679eb993137bc69b2aea51d10fb31fe25efa631dfcbe5c153aa516cf3b35a07c744b24d43037211de466b66d4dfd55b7563cdf4a69b806bc7e66fa5fbb6ad67104454264884ee6792b8c58c719e1b557b370bfdc70c454ad1e85cef952f03d2aa5abf2352ce7deec7a5e02c5f0d1880529fb716cb43ca5c6bad2bdfc9796948c84be45a76c75599f6bace065fd132ac751b964dc7c7f095e1dd952f3d4801e350d72b49a897733b2a91ec122bfaab443b989194ddfacf6d866d32d7ea1fec48bf2e42321a30cdaa3f5b3d0a189a8ed90935954a08e6c84e75182768c8de581b6cf235afd8b6d8ee5417ced66a32a22a362ea93da8ed54de926b33c9abd2533c9ad5f0d130f0d99debd059e79f3075d9d9e0125ac2d3c5c135fa62b16c10d44125e1b3b9475e6491d2e7b346c18a596314da2d9f986b1a6ec046b826d8f156b5d6640bd5610f08193ed0eaf31691bb9898e74b2c7dc632fa796a5c466b2d92b20e1286267293d94ed499d39bed6e2a9a24d8410c9886b33707f8ae535e8ced544bfb6d0e789d03e805c4e0e4f35b9fa53a5866ec8a74e7e3206590f8a1cca9541ca8ad2f3ef96bdb601baefa7d6b451009bdf1542658c73';

function get_data(data){
return AES_Decrypt(data)
}
function get1_data(data){
return AES_Encrypt(data)
}
console.log(get_data(data))
//console.log(get1_data('12345678'))
// https://gkcx.eol.cn/school/102/provinceline
